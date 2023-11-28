def sqlUnsentMessages():
    return "SELECT ID, NUMERO, MENSAGEM, ID_ANEXO FROM MENSAGENS_WHATSAPP WHERE ENVIO IS NULL AND COD_ERRO IS NULL AND ERRO IS NULL"


def sqlSelectAnexosById(id):
    return "SELECT ID, SEQ, ARQUIVO FROM ANEXOS_WHATSAPP WHERE ID = %i" % (id)


def sqlUpdateMessageError(messageId, errorCode, errorMessage):
    return f"""
      UPDATE MENSAGENS_WHATSAPP SET
         COD_ERRO = {errorCode},
         ERRO = '{errorMessage}'
      WHERE 
         ID = {messageId} 
      """


def sqlUpdateAnexoError(anexosId, anexosSeq):
    return f"""
      UPDATE ANEXOS_WHATSAPP SET 
         ERRO = 1
      WHERE 
         ID = {anexosId} AND
         SEQ = {anexosSeq}
      """


def sqlUpdateMessageEnvio(messageId, envio):
    return (
        "UPDATE MENSAGENS_WHATSAPP SET ENVIO = '%s', COD_ERRO = NULL, ERRO = NULL WHERE ID = %i"
        % (envio, messageId)
    )


def sqlUpdateWhatsappAguardandoQrCode(valor):
    return "UPDATE CONFIGURACOES2 SET WHATSAPP_AGUARDANDO_QRCODE = '%s' " % (valor)
