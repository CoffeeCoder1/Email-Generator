import json
import base64
from email.message import EmailMessage

from email_draft_generator.attachment import EmailAttachment
from email_draft_generator.email_list import EmailRecipient


class EmailTemplate:
	"""An E-mail template."""
	
	def __init__(
	    self,
	    *,
	    subject: str | None = None,
	    body: str | None = None,
	    attachments: [] = [],
	):
		"""Creates a new E-mail template."""
		self.subject = subject
		self.body = body
		self.attachments = attachments
	
	def __eq__(self, other):
		"""EmailTemplate objects are considered equal if they have the same contents."""
		if type(self) != type(other):
			return NotImplemented
		return vars(self) == vars(other)
	
	def __json__(self):
		"""Returns a dictionary for JSON serialization."""
		return self.__dict__
	
	def create_email_body(self, recipient: EmailRecipient):
		"""Uses the template to generate an E-mail body with the provided company."""
		mime_message = EmailMessage()
		
		# Add headers
		mime_message["To"] = recipient.email
		# Doesn't seem to be required for Gmail
		# mime_message["From"] = ""
		if self.subject != None:
			mime_message["Subject"] = str(self.subject).format_map(recipient.__dict__)
		
		# Add text
		mime_message.set_content(str(self.body).format_map(recipient.__dict__))
		
		# Add attachments
		for attachment in self.attachments:
			mime_message.add_attachment(attachment.data, maintype=attachment.maintype, subtype=attachment.subtype, filename=attachment.filename)
		
		encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
		
		return {"message": {"raw": encoded_message}}
	
	@classmethod
	def get_sample_template(cls):
		"""Returns a sample E-mail template."""
		return cls(
		    subject="Test E-mail",
		    body="""This is a template E-mail used to test an E-mail generation program. Please disregard.

company.name: {name}
company.email: {email}""",
		)
	
	@classmethod
	def from_dict(cls, dictionary: dict):
		"""Parses an E-mail template from a dictionary with keys 'subject', 'body', and 'attachments'."""
		template = cls(
		    subject=dictionary.get('subject'),
		    body=dictionary.get('body'),
		)
		template.attachments = []  # Make sure that there are no attachments left over from the previous run
		if 'attachments' in dictionary:
			for attachment in dictionary['attachments']:
				template.attachments.append(EmailAttachment.from_dict(attachment))
		return template
	
	@classmethod
	def from_file(cls, file):
		"""Parses an E-mail template out of a JSON file."""
		template_dict = json.load(file)
		template = cls.from_dict(template_dict)
		return template
