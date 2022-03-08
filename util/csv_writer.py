import csv, os
from email.policy import default
from datetime import datetime
from global_values import OUTPUT_FOLDER


default_file_name = f"{OUTPUT_FOLDER}/hour-{datetime.now().hour}.csv"

def __open_csv_file(file_name = default_file_name) -> bool:
    success = False

    if os.path.exists(file_name):
        return True

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    _f = open(file_name, "x")
    if _f:
        success = True
    _f.close()
        
    return success

def __verify_csv_has_headers(file_name = default_file_name) -> bool:
    sniffer = csv.Sniffer()
    with open(file_name, mode = "r") as _f:
        sample = _f.read(1024)
        if len(sample) == 0:
            return False

        return sniffer.has_header(sample)


def write_csv_line(output_dict: dict, file_name = default_file_name):
    if not __open_csv_file(file_name):
        print(f"Failed to open {file_name}")
        return
    
    with open(file_name, "a", newline="") as _csv_file:
        field_names = output_dict.keys()

        writer = csv.DictWriter(_csv_file, fieldnames=field_names)

        if not __verify_csv_has_headers(file_name):
            writer.writeheader()

        writer.writerow(output_dict)