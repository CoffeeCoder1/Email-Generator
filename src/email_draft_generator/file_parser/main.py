import sys
import argparse
import json
import json_fix

from email_draft_generator.file_parser import text_parser
from email_draft_generator.file_parser import csv_parser


def main():
	# Command-line arguments
	parser = argparse.ArgumentParser(prog='email-list-parser', description='Takes a list of E-mail addresses and turns it into a JSON file.')
	
	parser.add_argument('--format', choices=['text', 'csv'], default='text', help='the format of the input file (default: text)')
	parser.add_argument('infile', type=argparse.FileType('r'), help='the list of e-mail addresses to parse')
	
	args = parser.parse_args()
	
	try:
		if args.format == 'text':
			recipients = text_parser.parse(args.infile.readlines())
		elif args.format == 'csv':
			recipients = csv_parser.parse(args.infile)
		else:
			recipients = None
		
		if recipients != None:
			json.dump(recipients, sys.stdout, indent="\t")
		else:
			raise ValueError("Unsupported filetype!")
	except:
		raise ValueError("Invalid input file")
