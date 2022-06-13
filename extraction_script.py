import csv

skipping = False

output_path_one = "extracted_from_tfs.txt"
output_path_two = "sanitized_from_tfs.txt"

skip_text = ["file_name_set", "serial_received", "serial_connected", "Running", "Port", "Serial"]
unskip_text = ["qr_code_set", "Start test"]

def round_one():
    with open("output/07-06-2022/hour-13.txt", "r") as input_file:
        
        for line in input_file:
            if "rst:0x1" in line:
                skipping = True
                print("HELLO")

            elif "Initiating Si7051 Library" in line:
                skipping = False
                continue

            if not skipping:
                with open (output_path_one, mode="a") as output_file:
                    output_file.write(line)

def round_two():
    with open(output_path_one, mode="r") as input_file:
        for line in input_file:
            if any(x in line for x in skip_text):
                if any(y in line for y in unskip_text):
                    with open (output_path_two, mode="a") as output_file:
                        output_file.write(line)
                continue
            
            with open (output_path_two, mode="a") as output_file:
                    output_file.write(line)

if __name__ == "__main__":
    round_two()
    