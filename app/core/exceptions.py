class AlreadyExistsException(Exception):
    def __init__(self, message="El recurso ya existe"):
        self.message = message
        super().__init__(self.message)
