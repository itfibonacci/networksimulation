import logging
from abc import ABC, abstractmethod
from exceptions import WrongIPAddressFormat, DuplicateIPAddressException, IPAddressNotFoundException
import re
import time
import threading
import sys
import queue

class Machine(ABC):

	used_ip_addresses = set()
	all_machines = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		
		if not self.check_ip_address_format(ip_address):
			raise WrongIPAddressFormat(ip_address)

		if ip_address in self.__class__.used_ip_addresses:
			raise DuplicateIPAddressException(ip_address)
		else:
			self.__class__.used_ip_addresses.add(ip_address)
			self.__class__.all_machines[ip_address] = self

		self.ip_address = ip_address
		self.port = port
		self.incoming_capacity = incoming_capacity
		self.outgoing_capacity = outgoing_capacity
		self.incoming_requests = 0
		self.outgoing_requests = 0
		self.incoming_queue = queue.Queue(self.incoming_capacity)
		self.outgoing_queue = queue.Queue(self.outgoing_capacity)
		self.status = "Stopped"
	
	@classmethod
	def ip_address_exists(cls, ip_address):
		if ip_address in Machine.used_ip_addresses:
			return True
		else:
			raise False
	
	@classmethod
	def find_machine_by_ip(cls, ip_address):
		if ip_address in Machine.all_machines:
			return Machine.all_machines[ip_address]
		else:
			raise IPAddressNotFoundException(ip_address)
	
	def print_load(self):
		while self.status == "Running":
			sys.stdout.write(f"\rMachine {self.ip_address} - Incoming load: {self.get_machine_incoming_load()}%, Outgoing load: {self.get_machine_outgoing_load()}%")
			sys.stdout.flush()
			#print(f"Incoming load: {self.get_machine_incoming_load()}%")
			#print(f"Outgoing load: {self.get_machine_outgoing_load()}%")
			# Wait for 1 second
	
	def start_printing_load(self):
		print_load_thread = threading.Thread(target=self.print_load)
		print_load_thread.start()
	
	def get_machine_incoming_load(self):
		return (self.incoming_requests/self.incoming_capacity)*100
	
	def get_machine_outgoing_load(self):
		return (self.outgoing_requests/self.outgoing_capacity)*100
	
	def check_ip_address_format(self, ip_address):
		ip_address_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
		if not re.match(ip_address_pattern, ip_address):
			return False
		else:
			return True

	def start(self):
		if self.status == "Stopped":
			self.status = "Running"
			logging.info(f"[{self.ip_address}]:{self.__class__.__name__} started")
			#self.start_printing_load()
		elif self.status == "Running":
			logging.warn(f"[{self.ip_address}]:{self.__class__.__name__} has been started already.")
	
	@abstractmethod
	def stop(self):
		pass
