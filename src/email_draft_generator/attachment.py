import os
import mimetypes


class EmailAttachment:
	
	def __init__(self, *, data, path: os.PathLike, filename: str | None = None):
		self.data = data
		self.path = path
		# If the filename is None, default to the name of the source file
		if filename == None:
			self.filename = os.path.basename(path)
		else:
			self.filename = filename
		
		type_subtype, _ = mimetypes.guess_type(path)
		self.maintype, self.subtype = type_subtype.split("/")
	
	@classmethod
	def from_path(cls, path: os.PathLike, filename: str | None = None):
		with open(path, "rb") as fp:
			data = fp.read()
		
		return cls(data=data, path=path, filename=filename)
	
	@classmethod
	def from_dict(cls, dictionary: dict):
		return cls.from_path(path=dictionary.get('path'), filename=dictionary.get('filename'))
