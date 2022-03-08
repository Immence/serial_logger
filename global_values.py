import os, sys

from datetime import date

from queue import Queue

WIN_WIDTH, WIN_HEIGHT = 684, 400
SER_TIMEOUT = 0.1
RETURN_CHAR = "\n"
PASTE_CHAR = "\x16"
BAUD_RATE = 115200
TEXT_SIZE = 14
OUTPUT_FOLDER = os.path.abspath(os.path.join(sys.argv[0], os.path.pardir, "output", date.today().strftime("%d-%m-%Y")))
QC_OUTPUT_FOLDER = os.path.abspath(os.path.join(sys.argv[0], os.path.pardir, "output_qc", date.today().strftime("%d-%m-%Y")))
COMMAND_QUEUE = Queue()