# instead of having clients send requests to an ip address, the client should send a request to a fqdn.
# which then goes to the dns server the dns will return the ip address of a client
# eventually maybe caching will be utilized
from server import Server

class dns(Server):
	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
	
	def return_ip_address(self, fqdn):
		pass