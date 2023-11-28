# Libs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Local source
from utils.dataBaseUtils import SQLHandler
from utils.sysUtils import logAndPrint
from utils.messagesUtils import formatInvalidEmailRows
from repositories.emailRepositories import sqlSelectEmailConfig
from config.globals import getConnection


class invalidEmailDataException(Exception):
   def __init__(self, invalidRows):
      self.invalidRows = invalidRows


class intelectualSysEmail:
   def __init__(self):
      try:
         self.emailConfig = self.getEmailConfigFromDataBase()

         self.msg = MIMEMultipart()
         self.msg['From'] = self.emailConfig.senderEmail

      except invalidEmailDataException as e:
         logAndPrint(formatInvalidEmailRows(e.invalidRows))

      except Exception as e:
         print(str(e))

   
   def getEmailConfigFromDataBase(self):
      try:
         sqlHandler = SQLHandler(getConnection())
         emailConfigData = sqlHandler.fetchOne(sqlSelectEmailConfig())

         senderEmail = emailConfigData[0]
         port = emailConfigData[1]
         host = emailConfigData[2]
         senderPassword = emailConfigData[3]

         return emailConfig(senderEmail, port, host, senderPassword)
         
      finally:
         sqlHandler.close()


   def addMessage(self, emailMessage):
      text = MIMEText(emailMessage)
      self.msg.attach(text)

   
   def addImage(self, imageFile):
      with open(imageFile, 'rb') as fp:
         img = MIMEImage(fp.read())
      
      img.add_header('Content-Disposition', 'attachment', filename='image.jpg')
      self.msg.attach(img)


   def setRecipient(self, recipientEmail):
      self.msg['To'] = recipientEmail


   def setSubject(self, emailSubject):
      self.msg['Subject'] = emailSubject


   def send(self):
      try:
         server = smtplib.SMTP(self.emailConfig.smtpServer, self.emailConfig.smtpPort)
         server.starttls()
         server.login(self.emailConfig.senderEmail, self.emailConfig.senderPassword)
         server.send_message(self.msg)
      finally:
         server.quit()


class emailConfig():
   def __init__(self, senderEmail, smtpPort, smtpServer, senderPassword):
      invalidRows = []

      self.senderEmail = senderEmail if senderEmail is not None else invalidRows.append('Email')
      self.smtpPort = smtpPort if smtpPort is not None else invalidRows.append('Porta SMTP')
      self.smtpServer = smtpServer if smtpServer is not None else invalidRows.append('Servidor SMTP')
      self.senderPassword = senderPassword if senderPassword is not None else invalidRows.append('Senha do Email')

      if len(invalidRows) > 0:
         raise invalidEmailDataException(invalidRows)

    