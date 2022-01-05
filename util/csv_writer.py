import csv, os

from global_values import OUTPUT_FOLDER


file_name = f"{OUTPUT_FOLDER}/output.csv"

def __open_csv_file() -> bool:
    success = False

    if os.path.exists(file_name):
        return True

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    _f = open(file_name, "x")
    if _f:
        success = True
    _f.close()
        
    return success

def __verify_csv_has_headers() -> bool:
    sniffer = csv.Sniffer()
    with open(file_name, mode = "r") as _f:
        sample = _f.read(1024)
        if len(sample) == 0:
            return False

        return sniffer.has_header(sample)


def write_csv_line(output_dict: dict):
    if not __open_csv_file():
        print(f"Failed to open {file_name}")
        return
    
    with open(file_name, "a", newline="") as _csv_file:
        field_names = output_dict.keys()

        writer = csv.DictWriter(_csv_file, fieldnames=field_names)

        if not __verify_csv_has_headers():
            writer.writeheader()

        writer.writerow(output_dict)