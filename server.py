from abc import ABC, abstractmethod
import logging
import time
import threading
from queue import Empty

from message import Message
from machine import Machine
from exceptions import MachineNotRunningException, IPAddressNotFoundException

class Server(Machine, ABC):
	all_servers = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_servers[ip_address] = self
	
	def process_incoming_queue(self):
		while self.status == "Running":
			try:
				client_request = self.incoming_queue.get(timeout=1)
				logging.info(f"[{self.ip_address}]:Processing request from incoming queue: {client_request.id}")
				response = self.create_response_message(client_request)
				self.queue_outgoing_message(response)
			except Empty:
				continue

	def create_response_message(self, client_message):
		response_content = f"Response to the message: {client_message.message_content}"
		response = Message(origin_address = self.ip_address, destination_address = client_message.get_origin_address(), message_content = response_content)
		return response

	def stop(self):
		self.status = "Stopped"
		self.process_incoming_queue_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_incoming_queue_thread.getName()}")
		self.process_outgoing_queue_thread.join()
		logging.info(f"[{self.ip_address}]:Stopped thread: {self.process_outgoing_queue_thread.getName()}")
	
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
