import csv
import concurrent.futures

from email_draft_generator.email_list import EmailRecipient


def parse(data):
	"""Takes a CSV file with fields `name,email` and parses it into a list of recipients."""
	recipients = []
	reader = csv.DictReader(data, fieldnames=["name", "email"])
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for row in reader:
			recipients.append(EmailRecipient.from_dict(row))
	return recipients
