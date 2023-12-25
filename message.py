from uuid import uuid4

class Message():
	def __init__(self, origin_address, destination_address, message_content ) -> None:
		self.id = uuid4()
		self.origin_address = origin_address
		self.destination_address = destination_address
		self.message_content = message_content
	
	def get_origin_address(self):
		return self.origin_address
	
	def get_destination_address(self):
		return self.destination_address

class dnsMessage(Message):
	def __init__(self, origin_address, dns_server, message_content, request_type) -> None:
		super().__init__(origin_address, dns_server, message_content, request_type)
		self.request_type = request_type
