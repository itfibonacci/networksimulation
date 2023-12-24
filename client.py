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

	def process_incoming_queue(self):
		while self.status == "Running":
			try:
				response = self.incoming_queue.get(timeout=1)
				logging.info(f"[{self.ip_address}]:Processing response: {response.id}")
			except Empty:
				continue

	def send_request(self, destination_address, message_content):
		request = Message(self.ip_address, destination_address, message_content)
		self.queue_outgoing_message(request)

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
