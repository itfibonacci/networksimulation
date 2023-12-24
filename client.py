import logging
import time
import threading
from queue import Empty

from message import Message
from machine import Machine
from exceptions import IPAddressNotFoundException

# We can add a stat to the client of how many messages were sent and how many received.

class Client(Machine):
	all_clients = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_clients[ip_address] = self

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
		logging.info(f"{self.outgoing_queue.get()}")

	def process_outgoing_requests(self):
		while self.status == "Running":
			try:
				message = self.outgoing_queue.get(timeout=1)
				server_to_send = Machine.find_machine_by_ip(message.get_destination_address())
				server_to_send.queue_request(message)
				logging.info(f"[{self.ip_address}]:Sent request: {message.id} to server: {message.get_destination_address()}")
			except Empty:
				continue

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
			try:
				response = self.incoming_queue.get(timeout=1)
				logging.info(f"[{self.ip_address}]:Processing response: {response.id}")
			except Empty:
				continue

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
	
	def start(self):
		super().start()
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

	def stop(self):
		self.status = "Stopped"
		self.process_outgoing_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_outgoing_thread.getName()}")
		self.process_response_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_response_thread.getName()}")
