import re

searchable = "# Device identity:# QR-Code: B3-H-0016 Hardware ID: B50OFLIYS6BWFS0LSA5H Device Variant: b2-h"

if __name__ == "__main__":
    print(f"Searching in string {searchable}")
    print(re.search("B[0-9]+-[A-Z]+-[0-9]{4,}", searchable).group(0))