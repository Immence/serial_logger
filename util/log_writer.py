from email.policy import default
import os
from datetime import datetime
from global_values import OUTPUT_FOLDER
import time

default_file_name = f"{OUTPUT_FOLDER}/hour-{datetime.now().hour}.txt"

def __open_log_file(file_name) -> bool:
    success = False

    if os.path.exists(file_name):
        return True

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    _f = open(file_name, "x")
    if _f:
        success = True
    _f.close()
        
    return success

def write_log_line(text: str, file_name : str = default_file_name):

    if not __open_log_file(file_name):
        print(f"Failed to open {file_name}")
        return

    with open(file_name, "a") as log_file:
        log_file.write(f"{int(time.time())} | {text}\n")
        