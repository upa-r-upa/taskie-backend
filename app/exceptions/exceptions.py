class DataNotFoundError(Exception):
    def __init__(self, message: str = "The requested data was not found"):
        self.message = message
        super().__init__(self.message)
