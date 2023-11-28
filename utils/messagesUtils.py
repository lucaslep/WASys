from constants.dbConstants import *
from constants.genericConstants import *

def formatSQLExecError(sql, message):
   return (
      DB_SQL_EXEC_ERROR + \
      sql + \
      WITH_MESSAGE + \
      message)
   

def formatSQLReadError(sql, message):
   return (
      DB_SQL_READ_ERROR + \
      sql + \
      WITH_MESSAGE + \
      message)


def formatDbConnectError(message):
   return(
      DB_CONNECT_ERROR + \
      message
   )


def formatDataAcessError(message):
   return(
      DB_DATA_ACESS_ERROR + \
      message
   )


def formatMessageSendSuccess(number):
   return f"Mensagem para o número {number} enviada com sucesso!"


def formatInvalidNumberError(idMessage, number):
   return f"Não foi possivel enviar a mensagem com id: {idMessage} devido ao numero: {number} inválido"


def formatFileNotFoundError(idMessage, file):
   return f"Não foi possivel enviar a mensagem com id: {idMessage} devido ao arquivo não encontrado: {file}"


def formatInvalidEmailRows(invalidRows):
   baseMessage = "Não foi possivel enviar o email devido aos campos inválidos nas configurações: "
   separator = ", "
   invalidRowStr = separator.join(invalidRows)

   return baseMessage + invalidRowStr
