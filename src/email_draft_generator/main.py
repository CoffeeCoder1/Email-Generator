import os

import json
import concurrent.futures
import argparse

import email_draft_generator.gmail
import email_draft_generator.mail_util
import email_draft_generator.email_creator

def main():
	# Command-line arguments
	parser = argparse.ArgumentParser(
		prog='email-generator',
		description='Generates E-mail drafts from a list of E-mail addresses and uploads them to Gmail.'
	)

	parser.add_argument('-t', '--template', type=argparse.FileType('r'), help='the template file to use')
	parser.add_argument('infile', type=argparse.FileType('r'), help='the list of e-mail addresses to parse')

	args = parser.parse_args()

	# TODO: Use a keyring for these
	global_creds_dir = os.path.expanduser("~/.local/share/email-generator/credentials")
	global_token_path = f"{global_creds_dir}/token.json"
	global_creds_path = f"{global_creds_dir}/credentials.json"

	# Load the companies from the JSON file
	print("Processing input data")
	companies = json.load(args.infile)

	# Load the template, or use the default if none is provided
	if args.template:
		template = json.load(args.template)
		print("Template loaded from file")
	else:
		template = email_draft_generator.email_creator.get_sample_template()
		print("No template provided! Sample template was used")

	# Authenticate with Google
	print("Authenticating")
	creds = email_draft_generator.gmail.get_creds(global_token_path, global_creds_path)

	# Build all of the attachments
	attachments = []
	if 'attachments' in template:
		print("Processing attachments")
		with concurrent.futures.ProcessPoolExecutor() as executor:
			for attachment_path in template['attachments']:
				attachments.append(email_draft_generator.mail_util.build_attachment(attachment_path))

	print("Generating and uploading E-mails")
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for company in companies:
			email_draft_generator.gmail.create_draft(creds, email_draft_generator.email_creator.create_email_body(template, company, attachments))