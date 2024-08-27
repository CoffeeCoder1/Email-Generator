import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def get_oauth_flow(global_creds_path, creds_path=None):
	"""Get an OAuth2 flow from the specified credentials, copying them to the global location if they are not already there."""
	if not os.path.exists(global_creds_path) and creds_path:
		# If the global credentials do not exist, copy the provided credentials there
		input_path = Path(creds_path)
		with open(input_path, "r") as creds_input:
			oauth_creds = creds_input.read()
		
		flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
		
		output_path = Path(global_creds_path)
		output_path.parent.mkdir(parents=True, exist_ok=True)
		with open(global_creds_path, "w") as creds_output:
			creds_output.write(oauth_creds)
		
		input_path.unlink(missing_ok=True)
	else:
		# If they do, create an OAuth flow
		flow = InstalledAppFlow.from_client_secrets_file(global_creds_path, SCOPES)
	return flow


def get_token(token_path):
	"""Get the user's OAuth2 token and refresh it if it is expired."""
	# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
	if os.path.exists(token_path):
		creds = Credentials.from_authorized_user_file(token_path, SCOPES)
		# Refresh expired creds
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
	else:
		creds = None
	return creds


def write_token(creds, token_path):
	"""Sets the user's token globally."""
	output_path = Path(token_path)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with open(token_path, "w") as token:
		token.write(creds.to_json())


def get_creds(token_path, creds_path):
	"""Gets the user's Gmail credentials, asking for input on the command line where necessary."""
	creds = get_token(token_path)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		# Create new creds
		# If OAuth2 creds do not exist, tell the user to create them
		if not os.path.exists(creds_path):
			creds_path_input = input("No OAuth2 Credentials exist!\nFollow the guide at https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment to create them, and, when you are at the step to configure the OAuth consent screen, add the `gmail.compose` scope.\nDownload them to your device, copy the file path, and enter it here: ")
			flow = get_oauth_flow(creds_path, creds_path_input)
		else:
			flow = get_oauth_flow(creds_path)
		creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		write_token(creds, token_path)
	return creds


def create_draft(creds, body):
	"""Creates an email draft with the provided body"""
	error_output = None
	try:
		# Create Gmail API client
		service = build("gmail", "v1", credentials=creds)
		
		# pylint: disable=E1101
		draft = (service.users().drafts().create(userId="me", body=body).execute())
		print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
	except HttpError as error:
		print(f"An error occurred: {error}")
		draft = None
		error_output = error
	return [draft, error_output]


def get_user_info(creds):
	"""Creates an email draft with the provided body"""
	try:
		# Create Gmail API client
		service = build("gmail", "v1", credentials=creds)
		
		profile = service.users().getProfile(userId='me').execute()
	except HttpError as error:
		print(f"An error occurred: {error}")
		profile = None
	return profile
