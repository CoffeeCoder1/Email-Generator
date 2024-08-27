from email_draft_generator import gmail
from email_draft_generator.email_list import EmailRecipient
from email_draft_generator.email_template import EmailTemplate

import concurrent.futures
from tkinter import ttk


class EmailDrafter:
	"""Utility class to draft E-mails"""
	
	def __init__(self, error_button: ttk.Button | None = None):
		self.errors = []
		self.error_button = error_button
	
	def generate_drafts(self, recipients, template: EmailTemplate, creds, progressbar: ttk.Progressbar | None = None):
		self.errors = []
		with concurrent.futures.ProcessPoolExecutor() as executor:
			for recipient in recipients:
				draft = gmail.create_draft(creds, template.create_email_body(recipient))
				if draft[1] != None:
					self.errors.append(recipient)
					if self.error_button != None:
						self.error_button.config(state='normal')
				if progressbar != None:
					progressbar.step()
		if progressbar != None:
			progressbar.destroy()
