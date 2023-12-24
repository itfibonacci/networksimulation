# instead of having clients send requests to an ip address, the client should send a request to a fqdn.
# which then goes to the dns server the dns will return the ip address of a client
# eventually maybe caching will be utilized


"""Resolve: This method would take a domain name as input and return the corresponding IP address.
ReverseResolve: This method would take an IP address as input and return the corresponding domain name.
AddRecord: This method would add a new DNS record to the server’s database.
DeleteRecord: This method would delete a DNS record from the server’s database.
UpdateRecord: This method would update an existing DNS record in the server’s database.
LookupRecord: This method would search for a DNS record in the server’s database.
ReloadZoneFiles: This method would reload the zone files from disk into memory."""

from server import Server

class DNS(Server):
	used_ip_addresses = set()
	all_machines = {}
	dns_records = {}

	def __init__(self, ip_address, port, outgoing_capacity, incoming_capacity):
		super().__init__(ip_address, port, outgoing_capacity, incoming_capacity)
	
	def resolve(self, fqdn):
		return DNS.dns_records[fqdn]

	def add_record(self, fqdn, ip_address):
		DNS.dns_records[fqdn] = list(ip_address)
