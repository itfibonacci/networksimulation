from abc import ABC, abstractmethod
import time

class MachineNotRunningException(Exception):
	def __init__(self, server) -> None:
		super().__init__(f"{server.id} is not in Running state")

class Machine(ABC):
	def __init__(self, id: int, ip_address, port, outgoing_capacity, incoming_capacity):
		if not isinstance(id, int):
			raise ValueError("id must be an integer")

		self.id = id
		self.ip_address = ip_address
		self.port = port
		self.outgoing_capacity = outgoing_capacity
		self.incoming_capacity = incoming_capacity
		self.incoming_requests = 0
		self.outgoing_requests = 0
		self.status = "Stopped"

	def start(self):
		self.status = "Running"
		print(f"{self.__class__.__name__} with id: {self.id} has been started.")

class Server(Machine, ABC):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, ip_address, port, outgoing_capacity, incoming_capacity)

	def handle_request(self, message):
		if (self.status != "Running"):
			raise MachineNotRunningException(self)
		
		while True:
			self.incoming_requests += 1
			self.incoming_capacity -= 1

	def send_response(self, destination_address):
		bulk_response = Message( self.ip_address, destination_address )

class ApplicationServer(Server):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, ip_address, port, outgoing_capacity, incoming_capacity)

class Message():
	def __init__(self, origin_address, destination_address ) -> None:
		self.origin_address = origin_address
		self.destination_address = destination_address

class Client(Machine):
	
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, ip_address, port, outgoing_capacity, incoming_capacity)

	def send_request(self, ):
		pass

	def receive_response(self):
		pass

ap1 = ApplicationServer(14552, "127.0.0.1", 65543, 1000, 10000)
ap1.start()
client1 = Client(12321, "124.0.0.1", 54432, 10, 10)
client1.start()

# client to have an ability to send a message, and the server respond to that message