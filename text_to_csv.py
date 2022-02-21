import sys, os, csv

lines = []

output = []

with open("./hour-14.txt", "r") as input_file:
    lines = input_file.readlines()

current_barcode = None
for line in lines:
    if line.startswith("[I]"):
        if "Device Token" in line:
            current_barcode = line[len(line)-10:len(line)-1]
        
    elif line.startswith("1"):
        reading = line.split()
        _d = { 
            "qr_code": current_barcode,
            "Frequency": None,
            "Temperature": None,
            "Compensated": None,
            "SG": None
        }
        _d["Frequency"] = reading[0]
        _d["Temperature"] = reading[2]
        _d["Compensated"] = reading[6]
        _d["SG"] = reading[8]
        output.append(_d)

with open("microbatch_station_3.csv", mode="w") as output_file:
    
    field_names = output[0].keys()

    writer = csv.DictWriter(output_file, fieldnames= field_names)

    writer.writeheader()
    for o in output:
        writer.writerow(o)
        


    