import os, sys

OUTPUT_FOLDER = "output"

file_name = os.path.abspath(os.path.join(sys.argv[0], os.path.pardir, os.path.pardir, "output", "output.csv"))

def open_log_file() -> bool:
    success = False

    if os.path.exists(file_name):
        return True

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    _f = open(file_name, "x")
    if _f:
        success = True
    _f.close()
        
    return success

def write_log(text):

    if not open_log_file():
        print(f"Failed to open {file_name}")
        return

    with open(file_name, "a") as log_file:
        log_file.write(text+"\n")
        