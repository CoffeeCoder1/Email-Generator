import re


class EmailRecipient:
	"""A recipient on the E-mail list."""
	
	def __init__(self, *, name="", email=""):
		self.name = name
		self.email = email
	
	def __json__(self):
		"""Returns a dictionary for JSON serialization."""
		return self.__dict__
	
	@classmethod
	def from_dict(cls, dictionary: dict):
		"""Creates an EmailRecipient from a dictionary with keys 'name' and 'email'."""
		return cls(name=dictionary.get('name'), email=dictionary.get('email'))
	
	@property
	def valid(self):
		"""Checks if the E-mail address is valid."""
		pattern = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
		return re.match(pattern, self.email) != None
