from abc import ABC, abstractmethod
import logging
import time
import threading

from message import Message
from machine import Machine
from exceptions import MachineNotRunningException, IPAddressNotFoundException

class Server(Machine, ABC):
	all_servers = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_servers[ip_address] = self
		# Thread for the incoming requests
		self.process_incoming_queue_thread = threading.Thread(target=self.process_incoming_queue)
		self.process_incoming_queue_thread.daemon = True
		self.process_incoming_queue_thread.start()
		logging.info(f"[{self.ip_address}]:Started thread: {self.process_incoming_queue_thread.getName()}")
		# Thread for the incoming responses from the server
		self.process_outgoing_queue_thread = threading.Thread(target=self.process_outgoing_queue)
		self.process_outgoing_queue_thread.daemon = True
		self.process_outgoing_queue_thread.start()
		logging.info(f"[{self.ip_address}]:Started thread: {self.process_outgoing_queue_thread.getName()}")
		
	def queue_request(self, message):
		if (self.status != "Running"):
			raise MachineNotRunningException(self)
		
		self.incoming_requests += 1
		self.incoming_capacity -= 1
		# Simulate processing the request
		#time.sleep(0.1)
		self.incoming_queue.put(message)
		logging.info(f"[{self.ip_address}]:Queued request: {message.id} from client: {message.get_origin_address()}")
		self.incoming_requests -= 1
		self.incoming_capacity += 1
	
	def process_incoming_queue(self):
		while self.status == "Running":
			client_request = self.incoming_queue.get()
			logging.info(f"[{self.ip_address}]:Processing request from incoming queue: {client_request.id}")
			response = self.create_response_message(client_request)
			self.queue_response(response)
	
	def create_response_message(self, client_message):
		response_content = f"Response to the message: {client_message.message_content}"
		response = Message(origin_address = self.ip_address, destination_address = client_message.get_origin_address(), message_content = response_content)
		return response
	
	def queue_response(self, response):
		# Send the response back to the client
		self.outgoing_requests += 1
		self.outgoing_capacity -= 1
		#time.sleep(0.1)
		self.outgoing_queue.put(response)
		# todo
		logging.info(f"[{self.ip_address}]:Queued response: {response.id} destined for client: {response.get_destination_address()}")
		self.outgoing_requests -= 1
		self.outgoing_capacity += 1
		
	def process_outgoing_queue(self):
		while self.status == "Running":
			response = self.outgoing_queue.get()
			logging.info(f"[{self.ip_address}]:Sending response: {response.id}")
			client = Machine.find_machine_by_ip(response.get_destination_address)
			client.queue_response(response)

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
