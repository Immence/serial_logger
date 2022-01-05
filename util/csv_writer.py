import csv, os, sys

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
    if not open_csv_file():
        print(f"Failed to open {file_name}")
        return
    
    with open(file_name, "a", newline="") as _csv_file:
        field_names = output_dict.keys()

        writer = csv.DictWriter(_csv_file, fieldnames=field_names)

        if not verify_csv_has_headers():
            writer.writeheader()

        writer.writerow(output_dict)