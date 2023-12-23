import logging
import time
import threading

from message import Message
from machine import Machine
from exceptions import IPAddressNotFoundException

# We can add a stat to the client of how many messages were sent and how many received.

class Client(Machine):
	all_clients = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_clients[ip_address] = self
		# Thread for the outgoing requests
		self.process_outgoing_thread = threading.Thread(target=self.process_outgoing_requests)
		self.process_outgoing_thread.daemon = True
		self.process_outgoing_thread.start()
		logging.info(f"[{self.ip_address}]:Started thread: {self.process_outgoing_thread.getName()}")
		# Thread for the incoming responses from the server
		self.process_response_thread = threading.Thread(target=self.process_response)
		self.process_response_thread.daemon = True
		self.process_response_thread.start()
		logging.info(f"[{self.ip_address}]:Started thread: {self.process_response_thread.getName()}")

	def send_request(self, destination_address, message_content):
		self.send_thread = threading.Thread(target=self._send_request, args=(destination_address, message_content))
		self.send_thread.daemon = True
		self.send_thread.start()
		logging.info(f"[{self.ip_address}]:Started thread: {self.send_thread.getName()}")

	def _send_request(self, destination_address, message_content):
		self.outgoing_requests += 1
		self.outgoing_capacity -= 1
		message = Message(origin_address = self.ip_address, destination_address = destination_address, message_content = message_content)
		self.outgoing_requests -= 1
		self.outgoing_capacity += 1
		self.outgoing_queue.put(message)
		logging.info(f"[{self.ip_address}]:Queued request: {message.id} to server: {message.get_destination_address()}")

	def process_outgoing_requests(self):
		while self.status == "Running":
			message = self.outgoing_queue.get()
			server_to_send = Machine.find_machine_by_ip(message.get_destination_address())
			server_to_send.queue_request(message)
			logging.info(f"[{self.ip_address}]:Sent request: {message.id} to server: {message.get_destination_address()}")

	def queue_response(self, response):
		self.incoming_requests += 1
		self.incoming_capacity -= 1
		#time.sleep(0.1)
		logging.info(f"[{self.ip_address}]:Queued response: {response.id} from server: {response.get_origin_address()}")
		self.incoming_queue.put(response)
		self.incoming_requests -= 1
		self.incoming_capacity += 1
	
	def process_response(self):
		while self.status == "Running":
			response = self.incoming_queue.get()
			logging.info(f"[{self.ip_address}]:Processing response: {response.id}")
		
	def send_request_continuously(self, destination_address, message_content):
		while self.status == "Running":
			self.send_request(destination_address, message_content)
			time.sleep(0.1)
		
	def send_request_bulk(self, destination_address, message_content, amount_of_messages):
		thread = threading.Thread(target=self._send_requests_bulk, args=(destination_address, message_content, amount_of_messages))
		thread.start()
	
	def _send_requests_bulk(self, destination_address, message_content, amount_of_messages):
		for _ in range(amount_of_messages):
			self.send_request(destination_address, message_content)
	
	def stop(self):
		self.status = "Stopped"
		self.process_outgoing_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_outgoing_thread.getName()}")
		self.process_response_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_response_thread.getName()}")


from os import makedirs, path
from datetime import datetime

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
    
    client1 = Client("124.0.0.1", 54432, 10, 10)
    client1.start()
    client1.send_request("127.0.0.1", "Hello World")
    #client1.stop()
    
    #ap1.stop()
    
    #client2.send_request_bulk("128.0.0.1", "Hello World", 1000)
    #client3.send_request_bulk("127.0.0.1", "Hello World", 1000)

if __name__ == "__main__":
    main()