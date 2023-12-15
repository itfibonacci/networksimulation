from abc import ABC, abstractmethod
import time

# implement deleting a machine and removing the ip address from the pool
# invalid ip address based on a regex pattern

class MachineNotRunningException(Exception):
	def __init__(self, server) -> None:
		super().__init__(f"{server.ip_address} is not in Running state")

class DuplicateIPAddressException(Exception):
	def __init__(self, ip_address) -> None:
		super().__init__(f"{ip_address} is already in use.")

class IPAddressNotFoundException(Exception):
	def __init__(self, ip_address) -> None:
		super().__init__(f"{ip_address} is not registered to any server.")

class Machine(ABC):
	used_ip_addresses = set()

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		# if not isinstance(id, int):
		# 	raise ValueError("id must be an integer")
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
	
	def find_server_by_ip(self, ip_address):
		if ip_address in Server.all_servers:
			return Server.all_servers[ip_address]
		elif ip_address in Client.all_clients:
			return Client.all_clients[ip_address]
		else:
			raise IPAddressNotFoundException(ip_address)

	def start(self):
		self.status = "Running"
		print(f"{self.__class__.__name__} with ip: {self.ip_address} has been started.")

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

	def send_response(self, destination_address):
		bulk_response = Message( self.ip_address, destination_address )

class ApplicationServer(Server):
	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)

class Message():
	def __init__(self, origin_address, destination_address, message_content ) -> None:
		self.origin_address = origin_address
		self.destination_address = destination_address
		self.message_content = message_content

class Client(Machine):
	all_clients = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_clients[ip_address] = self

	def send_request(self, destination_address, message_content ):
		server = self.find_server_by_ip(destination_address)
		message = Message(origin_address = self.ip_address, destination_address = destination_address, message_content = message_content)
		server.handle_request(message = message)

	def receive_response(self):
		pass

ap1 = ApplicationServer("127.0.0.1", 65543, 1000, 10000)
ap1.start()
ap2 = ApplicationServer("128.0.0.1", 65543, 1000, 10000)
ap2.start()

print(Server.all_servers)

client1 = Client("124.0.0.1", 54432, 10, 10)
client1.start()
client2 = Client("125.0.0.1", 54432, 10, 10)
client2.start()

#client1.send_request( destination_address, "message")

# client to have an ability to send a message, and the server respond to that message