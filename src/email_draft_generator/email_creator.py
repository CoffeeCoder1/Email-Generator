import base64
from email.message import EmailMessage

def create_email_body(template, company, attachments):
	"""Generates an E-mail with the provided template, company data, and attachments"""
	mime_message = EmailMessage()

	# Add headers
	mime_message["To"] = company['email']
	# Doesn't seem to be required for Gmail
	# mime_message["From"] = ""
	if 'subject' in template:
		mime_message["Subject"] = str(template['subject']).format_map(company)

	# Add text
	mime_message.set_content(str(template['body']).format_map(company))

	# Add attachments
	for attachment in attachments:
		mime_message.add_attachment(attachment['data'], maintype=attachment['maintype'], subtype=attachment['subtype'], filename=attachment['name'])

	encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

	return {"message": {"raw": encoded_message}}

def get_sample_template():
	"""Returns a sample E-mail template."""
	return {
			'subject': "Test E-mail",
			'body': """This is a template E-mail used to test an E-mail generation program. Please disregard.

company.name: {name}
company.email: {email}""",
	}