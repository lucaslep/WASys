class WhatsAppException(Exception):
    """Base exception for WhatsApp related errors"""
    pass

class WhatsAppDisconnectedException(WhatsAppException):
    """Raised when WhatsApp is disconnected or not reachable"""
    pass

class WhatsAppLoginTimeoutException(WhatsAppException):
    """Raised when login takes too long"""
    pass

class MessageSendException(WhatsAppException):
    """Raised when a message fails to send"""
    pass
