# main.py
import logging
from os import makedirs, path
from datetime import datetime

from server import ApplicationServer
from client import Client
from dns import DNS
# implement deleting a machine and removing the ip address from the pool
# invalid ip address based on a regex pattern
# dns servers
# make ip address a class/type

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

	dns1 = DNS("8.8.8.8", 54, 10, 10)
	dns1.add_record("www.amazon.com", "127.0.0.1")
	dns1.start()

	client1 = Client("124.0.0.1", 54432, 10, 10)
	client1.start()
	client1.send_request("127.0.0.1", "Hello World")

	dns1.stop()
	client1.stop()
	ap1.stop()

	#client2.send_request_bulk("128.0.0.1", "Hello World", 1000)
	#client3.send_request_bulk("127.0.0.1", "Hello World", 1000)

if __name__ == "__main__":
	main()
