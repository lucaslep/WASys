class InvalidAttachmentException(Exception):
    def __init__(
        self,
        message_id: int,
        attachment_id: int,
        attachment_sequence: int,
        file_name: str,
    ):
        self.message_id = message_id
        self.attachment_id = attachment_id
        self.attachment_sequence = attachment_sequence
        self.file_name = file_name
