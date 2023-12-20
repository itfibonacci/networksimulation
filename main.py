# main.py
import logging
from os import makedirs, path
from datetime import datetime

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
    print("Hello, world!")

if __name__ == "__main__":
    main()
