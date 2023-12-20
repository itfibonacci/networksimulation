class Message():
	def __init__(self, origin_address, destination_address, message_content ) -> None:
		self.origin_address = origin_address
		self.destination_address = destination_address
		self.message_content = message_content
	
	def get_origin_address(self):
		return self.origin_address
	
	def get_destination_address(self):
		return self.destination_address
