# main.py
import logging
from os import makedirs, path
from datetime import datetime

from server import ApplicationServer
from client import Client
# implement deleting a machine and removing the ip address from the pool
# invalid ip address based on a regex pattern

# Logging setup to log to a file
def get_log_filename():
	dir_name = "logs"
	# Check if the directory exists
	if not path.exists(dir_name):
		# If the directory doesn't exist, create it
		makedirs(dir_name)

	# Get current date and time
	now = datetime.now()

	# Format as a string
	date_time_str = now.strftime("%Y%m%d_%H%M%S")

	# Attach to a filename
	filename = f"{dir_name}/server_logs_{date_time_str}.txt"

	return filename

def main():
    # Your main program logic goes here
    logging.basicConfig(filename=get_log_filename(), encoding='utf-8', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    ap1 = ApplicationServer("127.0.0.1", 65543, 100, 100)
    ap1.start()
    ap2 = ApplicationServer("128.0.0.1", 65543, 1000, 10000)
    ap2.start()

    client1 = Client("124.0.0.1", 54432, 10, 10)
    client1.start()
    client2 = Client("125.0.0.1", 54432, 10, 10)
    client2.start()
    client3 = Client("126.0.0.1", 54432, 10, 10)
    client3.start()
    client1.send_request_bulk("127.0.0.1", "Hello World", 1000)
    client2.send_request_bulk("128.0.0.1", "Hello World", 1000)
    client3.send_request_bulk("127.0.0.1", "Hello World", 1000)

if __name__ == "__main__":
    main()
