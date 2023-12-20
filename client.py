import logging
import time

from message import Message
from machine import Machine
from exceptions import IPAddressNotFoundException

class Client(Machine):
	all_clients = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_clients[ip_address] = self

	def send_request(self, destination_address, message_content):
		self.outgoing_requests += 1
		self.outgoing_capacity -= 1
		server_to_send = Machine.find_machine_by_ip(destination_address)
		message = Message(origin_address = self.ip_address, destination_address = destination_address, message_content = message_content)
		self.outgoing_requests -= 1
		self.outgoing_capacity += 1
		logging.info(f"[{self.ip_address}]:Sent request: {message.id} to server: {message.get_destination_address()}")
		server_to_send.handle_request(message = message)

	def receive_response(self, message):
		self.incoming_requests += 1
		self.incoming_capacity -= 1
		time.sleep(0.1)
		logging.info(f"[{self.ip_address}]:Received response: {message.id} from server: {message.get_origin_address()}")
		self.incoming_requests -= 1
		self.incoming_capacity += 1
	
	def send_request_continuously(self, destination_address, message_content):
		while self.status == "Running":
			self.send_request(destination_address, message_content)
			time.sleep(0.1)
		
	def send_request_bulk(self, destination_address, message_content, amount_of_messages):
		for _ in range(amount_of_messages):
			self.send_request(destination_address, message_content)
