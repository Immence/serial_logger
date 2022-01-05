import csv

OUTPUT_FOLDER = "output"

with open(f"{OUTPUT_FOLDER}/output.csv", "w", newline="") as csvfile:
    field_names = ["Barcode", "Frequency", "Temperature"]
    w = csv.DictWriter(csvfile, fieldnames=field_names)

    w.writeheader()
    w.writerow({"Barcode": "B2-H-0000", "Frequency": "1337.69", "Temperature": "69"})
    w.writerow({"Frequency": "1337.69", "Temperature": "69"})
    w.writerow({"Barcode": "B2-H-0069", "Frequency": "1337.69"})