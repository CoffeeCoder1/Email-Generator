from email_draft_generator import gmail
from email_draft_generator.email_list import EmailRecipient
from email_draft_generator.email_template import EmailTemplate

import concurrent.futures


class EmailDrafter:
	"""Utility class to draft E-mails"""
	
	@classmethod
	def generate_drafts(cls, recipients, template: EmailTemplate, creds):
		with concurrent.futures.ProcessPoolExecutor() as executor:
			for recipient in recipients:
				gmail.create_draft(creds, template.create_email_body(recipient))
