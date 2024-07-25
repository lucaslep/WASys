class DriverInitException(Exception):
    def __init__(self, message):
        self.message = f"Erro ao iniciar o webdriver com a mensagem: \n {message}"
        super().__init__(self.message)
