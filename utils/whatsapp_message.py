class WhatsappMessage:
    def __init__(self, message_id, number, message, attachment_id):
        self.files = []
        self.message_id = message_id
        self.number = number
        self.message = message
        self.attachment_id = attachment_id

    def has_attachment(self):
        return self.attachment_id is not None and self.attachment_id > 0
