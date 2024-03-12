class InvalidNumberException(Exception):
    def __init__(self, message_id, number):
        self.message_id = message_id
        self.number = number
