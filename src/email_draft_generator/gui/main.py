import fileinput
import json
import mimetypes
import os
import concurrent.futures
from pathlib import Path
import threading

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from email_draft_generator import gmail
from email_draft_generator.gui import gmail_gui
from email_draft_generator.file_parser import csv_parser
from email_draft_generator.file_parser import text_parser
from email_draft_generator.email_drafter import EmailDrafter
from email_draft_generator.email_template import EmailTemplate
from email_draft_generator.email_list import EmailRecipient
from email_draft_generator.gui.template_editor import TemplateEditorPopup

# TODO: Use a keyring for these
global_creds_dir = os.path.expanduser("~/.local/share/email-generator/credentials")
global_token_path = f"{global_creds_dir}/token.json"
global_creds_path = f"{global_creds_dir}/credentials.json"


class App(tk.Frame):
	# Get creds if they exist, but do not prompt the user if they don't
	creds = gmail_gui.get_creds(global_token_path, global_creds_path)
	
	def __init__(self, master):
		# Set up a window
		super().__init__(master, padx=10, pady=10)
		self.pack()
		
		self.parent = master
		self.errors = []
		
		# Frame for the main app content
		frm = self
		frm.grid()
		
		# Create a template editor and hide it
		self.template_editor = TemplateEditorPopup(self)
		self.template_editor.withdraw()
		
		self.authenticate_button = ttk.Button(frm, text="Authenticate", command=self.authenticate_button_callback)
		self.authenticate_button.grid(column=0, row=0)
		self.account_label = ttk.Label(frm)
		self.account_label.grid(column=1, row=0, columnspan=2)
		
		ttk.Label(frm, text="Template").grid(column=0, row=1)
		ttk.Button(frm, text="Open", command=self.template_editor.template_editor.load_template).grid(column=1, row=1)
		ttk.Button(frm, text="Edit", command=self.edit_template).grid(column=2, row=1)
		
		ttk.Label(frm, text="E-mail list").grid(column=0, row=2)
		ttk.Button(frm, text="Open", command=self.load_email_list).grid(column=1, row=2)
		
		ttk.Button(frm, text="Draft E-mails", command=self.send_emails).grid(column=0, row=3)
		self.error_button = ttk.Button(frm, text="View Errors", command=self.view_errors, state="disabled")
		self.error_button.grid(column=1, row=3)
		
		self.update_authenticate_label()
		
		self.email_drafter = EmailDrafter(self.error_button)
	
	def authenticate_button_callback(self):
		"""Callback for the authentication button, logs out if already authenticated."""
		if not self.creds or not self.creds.valid:
			self.authenticate()
		else:
			self.log_out()
	
	def authenticate(self):
		self.creds = gmail_gui.get_creds(global_token_path, global_creds_path, root=self)
		self.update_authenticate_label()
	
	def log_out(self):
		if messagebox.askyesno("Log out?", "Would you like to log out?"):
			Path(global_token_path).unlink(missing_ok=True)
			self.creds = gmail_gui.get_creds(global_token_path, global_creds_path)  # Clear the credentials variable
			self.update_authenticate_label()
	
	def update_authenticate_label(self):
		"""Update the authenticate button text to show if you are logged in or not."""
		if not self.creds or not self.creds.valid:
			self.authenticate_button.config(text="Authenticate")
			self.account_label.config(text="")
		else:
			self.authenticate_button.config(text="Log Out")
			profile = gmail.get_user_info(self.creds)
			if profile != None:
				self.account_label.config(text=f"Logged in as {profile['emailAddress']}")
			else:
				self.account_label.config(text=f"Unable to retrieve E-mail address")
	
	def edit_template(self):
		"""Opens the template editor"""
		self.template_editor.show()
		# TODO: Fix the thing where the parent window is focused on return
		#self.parent.deiconify()
	
	def load_email_list(self):
		"""Opens an E-mail list"""
		email_list_path = filedialog.askopenfilename(title="Select E-mail list", filetypes=[("E-mail list files", ".json .csv .txt")])
		
		if email_list_path == None or email_list_path == '':
			return
		
		# Get the mimetype of the file so we can figure out how to parse it
		type_subtype, _ = mimetypes.guess_type(email_list_path)
		
		# Parse list
		with open(email_list_path) as email_list_file:
			if type_subtype == "text/json":
				# Load JSON data
				email_list_dict = json.load(email_list_file)
				
				# Convert the list of dictionaries to a list of recipients
				email_list = []
				with concurrent.futures.ProcessPoolExecutor() as executor:
					for recipient in email_list_dict:
						email_list.append(EmailRecipient.from_dict(recipient))
			
			elif type_subtype == "text/csv":
				# Load CSV data
				self.email_list = csv_parser.parse(email_list_file)
			elif type_subtype == "text/plain":
				# Load plaintext data
				self.email_list = text_parser.parse(email_list_file)
	
	def send_emails(self):
		# If not authenticated, prompt the user to authenticate
		if not self.creds or not self.creds.valid:
			self.authenticate()
		
		# If no email list was provided, load the email list
		if not hasattr(self, 'email_list'):
			self.load_email_list()
		
		self.drafting_progressbar = ttk.Progressbar(self, orient='horizontal', maximum=len(self.email_list), length=300)
		self.drafting_progressbar.grid(column=0, row=4, columnspan=3)
		
		# Thread allows the UI to continue to work while this runs
		t = threading.Thread(target=self.email_drafter.generate_drafts, args=(self.email_list, self.template_editor.template_editor.template_editor.template, self.creds, self.drafting_progressbar))
		t.start()
	
	def view_errors(self):
		if len(self.email_drafter.errors) > 1:
			message = f"There were {len(self.email_drafter.errors)} error while sending E-mails. Would you like to save this to a file, so you can fix them and send them again?"
		else:
			message = f"There was {len(self.email_drafter.errors)} errors while sending E-mails. Would you like to save these to a file, so you can fix them and send them again?"
		
		if messagebox.askyesno("Errors", message):
			error_output_path = filedialog.asksaveasfilename(title="Select where to save the list of failed E-mails", defaultextension=".json")
			if error_output_path == None or error_output_path == '':
				return
			with open(error_output_path, "w") as error_file:
				json.dump(self.email_drafter.errors, error_file)


def main():
	"""Tcl/Tk based GUI for email-draft-generator"""
	root = tk.Tk()
	root.title("E-mail Generator")
	root.resizable(False, False)
	app = App(root)
	app.mainloop()
