
from nintendo.nex import nat, notification, nintendo_notification, \
	authentication, secure, friends, common
import pkg_resources

import logging
logger = logging.getLogger(__name__)


class Settings:

	TRANSPORT_UDP = 0
	TRANSPORT_TCP = 1
	TRANSPORT_WEBSOCKET = 2
	
	field_types = {
		"prudp.transport": int,
		"prudp.version": int,
		"prudp.stream_type": int,
		"prudp.fragment_size": int,
		"prudp.resend_timeout": float,
		"prudp.ping_timeout": float,
		"prudp.silence_timeout": float,
		"prudp.signature_version": int,

		"kerberos.key_size": int,
		"kerberos.key_derivation": int,
		
		"common.int_size": int,
		
		"server.version": int,
		"server.access_key": str.encode
	}

	def __init__(self, filename=None):
		self.settings = {}
		self.reset()
		if filename:
			self.load(filename)
		
	def reset(self): self.load("default.cfg")
	def copy(self):
		copy = Settings()
		copy.settings = self.settings.copy()
		return copy
	
	def get(self, field): return self.settings[field]
	def set(self, field, value):
		if field not in self.field_types:
			raise ValueError("Unknown setting: %s" %field)
		self.settings[field] = self.field_types[field](value)

	def load(self, filename):
		filename = pkg_resources.resource_filename("nintendo", "files/%s" %filename)
		with open(filename) as f:
			linenum = 1
			for line in f:
				line = line.strip()
				if line:
					if "=" in line:
						field, value = line.split("=", 1)
						self.set(field.strip(), value.strip())
					else:
						raise ValueError("Syntax error at line %i" %linenum)
				linenum += 1


class BackEndClient:
	def __init__(self, access_key, version, settings=None):
		if settings:
			self.settings = settings.copy()
		else:
			self.settings = Settings()
		self.settings.set("server.access_key", access_key)
		self.settings.set("server.version", version)
		
		self.auth_client = None
		self.secure_client = None
		
		self.nat_traversal_server = nat.NATTraversalServer()
		self.notification_server = notification.NotificationServer()
		self.nintendo_notification_server = nintendo_notification.NintendoNotificationServer()

		self.protocol_map = {
			self.nat_traversal_server.PROTOCOL_ID: self.nat_traversal_server,
			self.notification_server.PROTOCOL_ID: self.notification_server,
			self.nintendo_notification_server.PROTOCOL_ID: self.nintendo_notification_server
		}
		
	def connect(self, host, port):
		self.auth_addr = host, port
		self.auth_client = authentication.AuthenticationClient(self)
		self.auth_client.connect(host, port)
		
	def close(self):
		self.auth_client.close()
		if self.secure_client:
			self.secure_client.close()
		
	def login(self, username, password, auth_info=None, login_data=None):
		if auth_info:
			self.auth_client.login_ex(username, password, auth_info)
		else:
			self.auth_client.login(username, password)

		ticket = self.auth_client.request_ticket()
		host = self.auth_client.secure_station["address"]
		port = self.auth_client.secure_station["port"]
		if host == "0.0.0.1":
			host, port = self.auth_addr
		
		self.secure_client = secure.SecureClient(self, ticket)
		self.secure_client.connect(host, port)
		if login_data:
			urls = self.secure_client.register_urls(login_data)
		else:
			urls = self.secure_client.register_urls()
		self.local_station, self.public_station = urls
		
	def login_guest(self):
		self.login("guest", "MMQea3n!fsik")
