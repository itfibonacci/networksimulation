from abc import ABC, abstractmethod
import time
import logging

class Client(Machine):
	all_clients = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
		self.__class__.all_clients[ip_address] = self

	def send_request(self, destination_address, message_content):
		self.outgoing_requests += 1
		self.outgoing_capacity -= 1
		server_to_send = self.find_machine_by_ip(destination_address)
		message = Message(origin_address = self.ip_address, destination_address = destination_address, message_content = message_content)
		self.outgoing_requests -= 1
		self.outgoing_capacity += 1
		logging.info(f"[{self.ip_address}]:Sent request: {message.message_content} to server: {message.get_destination_address()}")
		server_to_send.handle_request(message = message)

	def receive_response(self, message):
		self.incoming_requests += 1
		self.incoming_capacity -= 1
		time.sleep(0.1)
		logging.info(f"[{self.ip_address}]:Received response: {message.message_content} from server: {message.get_origin_address()}")
		self.incoming_requests -= 1
		self.incoming_capacity += 1

ap1 = ApplicationServer("127.0.0.1", 65543, 100, 100)
ap1.start()
ap2 = ApplicationServer("128.0.0.1", 65543, 1000, 10000)
ap2.start()

client1 = Client("124.0.0.1", 54432, 10, 10)
client1.start()
client2 = Client("125.0.0.1", 54432, 10, 10)
client2.start()
client3 = Client("126.0.0.1", 54432, 10, 10)
client2.start()

client1.send_request("127.0.0.1", "Hello World")
