import os

import json
import argparse

from email_draft_generator import gmail
from email_draft_generator.email_template import EmailTemplate
from email_draft_generator.email_drafter import EmailDrafter


def main():
	# Command-line arguments
	parser = argparse.ArgumentParser(prog='email-generator', description='Generates E-mail drafts from a list of E-mail addresses and uploads them to Gmail.')
	
	parser.add_argument('-t', '--template', type=argparse.FileType('r'), help='the template file to use')
	parser.add_argument('infile', type=argparse.FileType('r'), help='the list of e-mail addresses to parse')
	
	args = parser.parse_args()
	
	# TODO: Use a keyring for these
	global_creds_dir = os.path.expanduser("~/.local/share/email-generator/credentials")
	global_token_path = f"{global_creds_dir}/token.json"
	global_creds_path = f"{global_creds_dir}/credentials.json"
	
	# Load the companies from the JSON file
	print("Processing input data")
	recipients = json.load(args.infile)
	
	# Load the template, or use the default if none is provided
	if args.template:
		template = EmailTemplate.from_file(args.template)
		print("Template loaded from file")
	else:
		template = EmailTemplate.get_sample_template()
		print("No template provided! Sample template was used")
	
	# Authenticate with Google
	print("Authenticating")
	creds = gmail.get_creds(global_token_path, global_creds_path)
	
	print("Generating and uploading E-mails")
	email_drafter = EmailDrafter()
	email_drafter.generate_drafts(recipients, template, creds)
