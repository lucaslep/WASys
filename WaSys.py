# LOCAL SOURCE
from utils.whatsAppUtils import getUnsentMessages, sendWhatsAppMessages
from utils.dataBaseUtils import intelectualSysDB
from utils.sysUtils import logAndPrint, exitWithLog
from config.globals import (
    setConnection,
    setApplicationPathAndDir,
    getApplicationPath,
    getApplicationDir,
)

import time


logAndPrint("Bem vindo! " + "Iniciando WaSys ... " + "Powered By Sóftica Informática ©")
logAndPrint("Conectando ao Banco de dados...")
try:
    setApplicationPathAndDir(__file__)

    dataBase = intelectualSysDB()
    con = dataBase.connect()
    setConnection(con)

    logAndPrint("Conexão com o banco efetuada com sucesso!")

    while True:
        unsentMessages = getUnsentMessages()
        messagesCount = len(unsentMessages)

        if messagesCount > 0:
            logAndPrint(f"Foram encontradas {messagesCount} mensagens a serem enviadas")
            sendWhatsAppMessages(unsentMessages)
        else:
            logAndPrint("Nenhuma mensagem a ser enviada ... Aguardando novas mensagens")

        time.sleep(10)

except Exception as e:
    logAndPrint(str(e))

finally:
    dataBase.disconnect()
    exitWithLog("Encerrando módulo WhatsApp, até mais!")
