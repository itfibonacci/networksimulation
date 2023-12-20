class MachineNotRunningException(Exception):
	def __init__(self, server) -> None:
		super().__init__(f"{server.ip_address} is not in Running state")

class WrongIPAddressFormat(Exception):
	def __init__(self, ip_address) -> None:
		super().__init__(f"{ip_address} is not in the correct format. Should be like: '127.0.0.1'")

class DuplicateIPAddressException(Exception):
	def __init__(self, ip_address) -> None:
		super().__init__(f"{ip_address} is already in use.")

class IPAddressNotFoundException(Exception):
	def __init__(self, ip_address) -> None:
		super().__init__(f"{ip_address} is not registered to any server.")
