# Libs.
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import urllib
import time

# Local
from repositories.whatsappRepositories import (
    sqlUnsentMessages,
    sqlSelectAnexosById,
    sqlUpdateMessageError,
    sqlUpdateAnexoError,
    sqlUpdateMessageEnvio,
    sqlUpdateWhatsappAguardandoQrCode,
)
from constants import whatsAppConstants as wppConsts
from config.globals import getConnection
from utils.messagesUtils import (
    formatInvalidNumberError,
    formatMessageSendSuccess,
    formatFileNotFoundError,
)
from utils.dataBaseUtils import SQLHandler
from utils.seleniumUtils import startWebDriver
from utils.fileUtils import fileExists
from utils.sysUtils import logAndPrint
from classes.email import intelectualSysEmail

# global variables
SEND_BTN_XPATH = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
SEND_FILE_BTN_XPATH = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'
INVALID_NUMBER_ELEMENT_XPATH = (
    '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
)
NO_CONTENT_FILE_ELE_XPATH = '//*[@id="app"]/div/span[1]/div/div/div[conatins(text(), "1 documento que você tentou adicionar não tem conteúdo.")]'


class whatsappNotLoggedException(Exception):
    pass


class invalidWhatsAppNumberException(Exception):
    def __init__(self, messageId, number):
        self.messageId = messageId
        self.number = number


class invalidMessageFilesException(Exception):
    def __init__(self, messageId, anexoId, anexoSeq, file):
        self.messageId = messageId
        self.anexoId = anexoId
        self.anexoSeq = anexoSeq
        self.file = file


class whatsApp:
    def __init__(self):
        self.driver = startWebDriver(visible=False)

        if not self.isLogged():
            self.logIn()

    def waitWhatsAppWebPageLoad(self, timeOut):
        wait = WebDriverWait(self.driver, timeOut)
        wait.until(EC.visibility_of_element_located((By.ID, "side")))

    def isLogged(self):
        try:
            self.driver.get("https://web.whatsapp.com/")
            self.waitWhatsAppWebPageLoad(35)

            return True

        except Exception as e:
            updateWhatsappWaitingQrCode("S")
            return False

    def logIn(self):
        logAndPrint("WhatsApp não logado, iniciando rotina de Login ... ")

        # reinicio o driver em modo visivel para poder visualizar o qr code
        self.driver.quit()
        self.driver = startWebDriver(visible=True)

        self.driver.get("https://web.whatsapp.com/")
        self.waitQrCodeToBeScanned()

        updateWhatsappWaitingQrCode("N")
        # Agora fecho o driver em primeiro plano e inicio novamente em background
        self.driver.quit()
        self.driver = startWebDriver(visible=False)

    def openConversationWithMessage(self, message):
        text = urllib.parse.quote(f"{message.mensagem}")
        whatsAppAPILink = (
            f"https://web.whatsapp.com/send?phone={message.numero}&text={text}"
        )
        self.driver.get(whatsAppAPILink)
        self.waitWhatsAppWebPageLoad(15)

    def sendMessage(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(EC.element_to_be_clickable((By.XPATH, SEND_BTN_XPATH))).click()

    def sendFiles(self, files):
        wait = WebDriverWait(self.driver, 10)

        for file in files:
            try:
                time.sleep(1)
                # Clica no clips
                clipElement = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div',
                        )
                    )
                )
                clipElement.click()

                # Localiza o Input de arquivos e envia os arquivos
                fileInputElement = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='file']")
                    )
                )
                fileInputElement.send_keys(file)

                # Clica no botão de envio
                sendFileBtn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, SEND_FILE_BTN_XPATH))
                )
                sendFileBtn.click()
            except Exception as e:
                logAndPrint(f"Ocorreram problemas ao enviar o arquivo: {file}:\n\n {e}")
                continue

    def send(self, message):
        self.openConversationWithMessage(message)

        time.sleep(2)

        if self.isWhatsAppNumberValid():
            self.sendMessage()

            if message.hasFiles():
                self.sendFiles(message.files)
        else:
            raise invalidWhatsAppNumberException(message.id, message.numero)

    def isWhatsAppNumberValid(self):
        try:
            element = self.driver.find_element(By.XPATH, INVALID_NUMBER_ELEMENT_XPATH)
            if element.text == "O número de telefone compartilhado por url é inválido.":
                return False
            else:
                return True

        except NoSuchElementException:
            return True

    def waitQrCodeToBeScanned(self):
        wait = WebDriverWait(self.driver, 10)
        element = None

        while not element:
            try:
                element = wait.until(EC.presence_of_element_located((By.ID, "side")))
                logAndPrint("Aguardando captura do QRCode para login ...")
            except:
                pass

        time.sleep(5)

    def quit(self):
        self.driver.quit()


class whatsAppMessage:
    def __init__(self, id, numero, mensagem, idAnexo):
        self.files = []
        self.id = id
        self.numero = numero
        self.mensagem = mensagem
        self.idAnexo = idAnexo

        if self.hasAnexoId():
            self.getFilesFromDB()

    def hasAnexoId(self):
        return self.idAnexo is not None and self.idAnexo > 0

    def getFilesFromDB(self):
        try:
            sqlHandler = SQLHandler(getConnection())
            anexosRows = sqlHandler.fetchAll(sqlSelectAnexosById(self.idAnexo))

            for anexoId, seq, file in anexosRows:
                if fileExists(file):
                    self.files.append(file)
                else:
                    raise invalidMessageFilesException(self.id, self.idAnexo, seq, file)
        finally:
            sqlHandler.close()

    def hasFiles(self):
        return len(self.files) > 0


def getUnsentMessages():
    unsentMessages = []
    try:
        sqlHandler = SQLHandler(getConnection())
        unsentMessagesRows = sqlHandler.fetchAll(sqlUnsentMessages())

        for id, numero, mensagem, idAnexo in unsentMessagesRows:
            try:
                message = whatsAppMessage(id, numero, mensagem, idAnexo)
                unsentMessages.append(message)

            except invalidMessageFilesException as e:
                handleInvalidMessageFileException(
                    e.messageId, e.anexoId, e.anexoSeq, e.file
                )
    finally:
        sqlHandler.close()

    return unsentMessages


def handleInvalidMessageFileException(messageId, anexoId, anexoSeq, file):
    try:
        logAndPrint(formatFileNotFoundError(messageId, file))

        sqlHandler = SQLHandler(getConnection())
        sqlHandler.executeQuery(
            sqlUpdateMessageError(
                messageId, wppConsts.ANEXOS_ERROR_CODE, wppConsts.ANEXOS_ERROR_MESSAGE
            )
        )
        sqlHandler.executeQuery(sqlUpdateAnexoError(anexoId, anexoSeq))

    except Exception as e:
        logAndPrint(str(e))

    finally:
        sqlHandler.close()


def handleInvalidNumberException(messageId, number):
    try:
        logAndPrint(formatInvalidNumberError(messageId, number))

        sqlHandler = SQLHandler(getConnection())
        sqlHandler.executeQuery(
            sqlUpdateMessageError(
                messageId,
                wppConsts.INVALID_NUMBER_ERROR_CODE,
                wppConsts.INVALID_NUMBER_MESSAGE,
            )
        )

    except Exception as e:
        logAndPrint(e)

    finally:
        sqlHandler.close()


def sendQrCodeByEmail(qrCodeImage):
    email = intelectualSysEmail()

    # email.setRecipient(email.emailConfig.senderEmail) # envio o email para a própria empresa
    email.setRecipient("icaro@softica.com.br")
    email.setSubject("QR Code para Login no WhatsApp - Sóftica Informática")
    email.addMessage(
        "Imagem do QR Code para login no WhatsApp, o QR Code pode se tornar inválido caso demore a ser utilizado"
    )
    email.addImage(qrCodeImage)

    email.send()


def markMessageAsSent(messageId):
    horaEnvio = datetime.now()
    horaEnvio = horaEnvio.strftime("%d.%m.%Y %H:%M:%S")

    try:
        sqlHandler = SQLHandler(getConnection())
        sqlHandler.executeQuery(sqlUpdateMessageEnvio(messageId, horaEnvio))

    except Exception as e:
        logAndPrint(str(e))

    finally:
        sqlHandler.close()


def sendWhatsAppMessages(messages):
    try:
        wpp = whatsApp()

        for message in messages:
            try:
                wpp.send(message)
                logAndPrint(formatMessageSendSuccess(message.numero))
                time.sleep(3)
                markMessageAsSent(message.id)

            except invalidWhatsAppNumberException as e:
                handleInvalidNumberException(e.messageId, e.number)
                continue

    finally:
        wpp.quit()


def updateWhatsappWaitingQrCode(value="N"):
    if value is None:
        raise Exception(
            'Nenhum valor informado para atualizar o campo "WHATSAPP_AGUARDANDO_QRCODE" '
        )

    value = value.upper()

    if value not in ["S", "N"]:
        raise Exception(
            'Valore do campo "WHATSAPP_AGUARDANDO_QRCODE" é inválido, a opção deve estar entre "S" ou "N"'
        )

    try:
        sqlHandler = SQLHandler(getConnection())
        sqlHandler.executeQuery(sqlUpdateWhatsappAguardandoQrCode(value))

    except Exception as e:
        logAndPrint(str(e))

    finally:
        sqlHandler.close()
