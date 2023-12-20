import logging
from abc import ABC, abstractmethod
from exceptions import WrongIPAddressFormat, DuplicateIPAddressException, IPAddressNotFoundException
import re

class Machine(ABC):
	used_ip_addresses = set()

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		
		if not self.check_ip_address_format(ip_address):
			raise WrongIPAddressFormat(ip_address)

		if ip_address in self.__class__.used_ip_addresses:
			raise DuplicateIPAddressException(ip_address)
		else:
			self.__class__.used_ip_addresses.add(ip_address)

		self.ip_address = ip_address
		self.port = port
		self.outgoing_capacity = outgoing_capacity
		self.incoming_capacity = incoming_capacity
		self.incoming_requests = 0
		self.outgoing_requests = 0
		self.status = "Stopped"
	
	@classmethod
	def find_machine_by_ip(cls, ip_address):
		if ip_address in Server.all_servers:
			return Server.all_servers[ip_address]
		elif ip_address in Client.all_clients:
			return Client.all_clients[ip_address]
		else:
			raise IPAddressNotFoundException(ip_address)
	
	def check_ip_address_format(self, ip_address):
		ip_address_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
		if not re.match(ip_address_pattern, ip_address):
			return False
		else:
			return True

	def start(self):
		self.status = "Running"
		logging.info(f"[{self.ip_address}]:{self.__class__.__name__} started")
