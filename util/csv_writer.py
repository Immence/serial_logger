import csv, os, sys
from datetime import datetime

OUTPUT_FOLDER = "output"

file_name = os.path.abspath(os.path.join(sys.argv[0], os.path.pardir, os.path.pardir, "output", "output.csv"))

def open_csv_file() -> bool:
    success = False

    if os.path.exists(file_name):
        return True

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    _f = open(file_name, "x")
    if _f:
        success = True
    _f.close()
        
    return success

def verify_csv_has_headers() -> bool:
    sniffer = csv.Sniffer()
    with open(file_name, mode = "r") as _f:
        sample = _f.read(1024)
        if len(sample) == 0:
            return False

        return sniffer.has_header(sample)


def write_csv_line(output_dict: dict):
    my_dict = {
        "Barcode": "B2-H-6969",
        "Frequency": "1000.69",
        "Temperature": "30"
    }

    if not open_csv_file():
        print(f"Could not open file {file_name}")
        return
    
    with open(file_name, "a", newline="") as _f:
        field_names = my_dict.keys()

        writer = csv.DictWriter(_f, fieldnames=field_names)

        if not verify_csv_has_headers():
            writer.writeheader()

        writer.writerow(my_dict)