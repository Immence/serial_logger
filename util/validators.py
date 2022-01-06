import re

class Validators():
    @staticmethod
    def validate_qr_code(qr: str) -> bool:
        match = re.match('B[0-9]+-[A-Z]+-[0-9]{4,}', str(qr))
        return bool(match)
