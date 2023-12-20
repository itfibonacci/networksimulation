from abc import ABC, abstractmethod
import logging
import time

from message import Message
from machine import Machine
from exceptions import MachineNotRunningException, IPAddressNotFoundException

class Server(Machine, ABC):
	all_servers = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_servers[ip_address] = self
		
	def handle_request(self, message):
		if (self.status != "Running"):
			raise MachineNotRunningException(self)
		
		self.incoming_requests += 1
		self.incoming_capacity -= 1
		# Simulate processing the request
		time.sleep(0.1)
		logging.info(f"[{self.ip_address}]:Received request: {message.id} from client: {message.get_origin_address()}")
		self.incoming_requests -= 1
		self.incoming_capacity += 1
		# Send the response back to the client
		self.create_response_message(message)
	
	def create_response_message(self, client_message):
		response_content = f"Response to the message: {client_message.message_content}"
		response = Message(origin_address = self.ip_address, destination_address = client_message.get_origin_address(), message_content = response_content)
		self.send_response(response)

	def send_response(self, message):
		# Send the response back to the client
		self.outgoing_requests += 1
		self.outgoing_capacity -= 1
		time.sleep(0.1)
		client = Machine.find_machine_by_ip(message.get_destination_address())
		# todo
		logging.info(f"[{self.ip_address}]:Sent response: {message.id} to client: {message.get_destination_address()}")
		self.outgoing_requests -= 1
		self.outgoing_capacity += 1
		client.receive_response(message)

class ApplicationServer(Server):
	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)

class DatabaseServer(Server):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, port, ip_address, outgoing_capacity, incoming_capacity)
		self.databases = []

	def create_database(self, database_name):
		self.database_name = self.databases.append(database_name)

class WebServer(Server):
	def __init__(self):
		pass
