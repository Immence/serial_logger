class InvalidFileNameException(Exception):
    
    def __init__(self, message="Invalid file name. Make sure the file name ends with .csv"):
        self.message = message
        super().__init__(self.message)

class InvalidQrCodeException(Exception):
    
    def __init__(self, message="Invalid QR-code"):
        self.message = message
        super().__init__(self.message)
