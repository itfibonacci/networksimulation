from machine import Machine
from exceptions import ServerNotRunningException 
from server import Server

class LoadBalancer(Machine):
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