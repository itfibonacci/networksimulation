from abc import ABC, abstractmethod
import time

"""
Server Type:
Identify the type of server you want to simulate. It could be a web server, application server, or database server. The functionality and behavior of the server will depend on its type.
1. Implement server capacity for each server say 100k requests per minute, beyond that write some function that degrades as the requests go up, if it goes up by too much have the server crash, also implement a random algorithm that crashes the servers in random intervals then comes up after a while, add server regions, add bootup time, add some sort of calculation of the time a request goes from one hop to another
2. Implement clients, can be still type server - have a variable that can be adjusted of how many requests they are sending to the server
3. loadbalancer types will have an ip address which then connects to a pool of servers. Loadbalance with a round robin
4. Implement Rate Limiters
5. send keepalive messages
"""
class ServerNotRunningException(Exception):
	def __init__(self, server) -> None:
		super().__init__(f"{server.id} is not in Running state")
	
class BulkMessage():
	def __init__(self, number_of_messages, origin_address, destination_address ) -> None:
		self.number_of_requests = number_of_messages
		self.origin_address = origin_address
		self.destination_address = destination_address

class Server(ABC):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		self.id = id
		self.ip_address = ip_address
		self.port = port
		self.outgoing_capacity = outgoing_capacity
		self.incoming_capacity = incoming_capacity
		self.status = "Stopped"
		self.incoming_requests = 0
		self.outgoing_requests = 0

	def handle_request(self, number_of_requests):
		if (self.status != "Running"):
			raise ServerNotRunningException(self)
		
		while True:
			self.incoming_requests += number_of_requests
			self.incoming_capacity -= number_of_requests

	def send_response(self, number_of_responses, destination_address):
		bulk_response = BulkMessage(number_of_responses, self.ip_address, destination_address )

	def start(self):
		self.status = "Running"
		print(f"{self.__class__.__name__} with id: {self.id} has been started.")

class DatabaseServer(Server):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, port, ip_address, outgoing_capacity, incoming_capacity)
		self.databases = []

	def create_database(self, database_name):
		self.database_name = self.databases.append(database_name)

class WebServer(Server):
	def __init__(self):
		super(self)
	
class ApplicationServer(Server):
	def __init__(self):
		super(self)

class Client():
	def __init__(self):
		pass

class LoadBalancer(Server):
	def __init__(self, id, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(id, port, ip_address, outgoing_capacity, incoming_capacity)
		self.outgoing_cluster = []

	def add_server_to_cluster(self, server):
		if (self.status != "Running"):
			raise ServerNotRunningException(self)
		
		if not isinstance(server, Server):
			raise ValueError(f"Invalid server type. Must be a subclass of Server but got {type(server).__name__}.")
		
		self.outgoing_cluster.append(server)
		print(f"Added {type(server).__name__} with id {server.server_id} to the cluster behind the load balancer {self.id}.")

dbserver = DatabaseServer(101231, "192.0.0.1", 5555, 10000, 1000)
#print(dbserver.handle_request("GET /request"))
dbserver.start()
print(dbserver.handle_request("GET /request"))
