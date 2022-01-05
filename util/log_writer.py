OUTPUT_FOLDER = "output"

def write_log(text):
    with open(f"{OUTPUT_FOLDER}/log.txt", "a") as log_file:
        log_file.write(text+"\n")
        