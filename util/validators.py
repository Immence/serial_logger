import re


def validate_qr_code(qr: str) -> bool:
    match = re.match('B[0-9]+-[A-Z]+-[0-9]{4}$', str(qr))
    return bool(match)

def validate_hardware_id(hardware_id: str) -> bool:
    match = re.match('[A-Z0-9]{20}', str(hardware_id))
    return bool(match)
