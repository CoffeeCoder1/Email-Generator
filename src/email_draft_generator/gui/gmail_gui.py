import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import webbrowser

from email_draft_generator import gmail


class CredsPopup(tk.Toplevel):
	
	def __init__(self, parent):
		super().__init__(parent)
		self.wm_title("OAuth2 Credentials")
		
		frm = ttk.Frame(self, padding=10)
		frm.grid()
		
		ttk.Label(self, text="No OAuth2 Credentials exist!").grid(row=0)
		ttk.Label(self, text="Follow the guide below to create them, and, when you are at the step to configure the OAuth consent screen, add the `gmail.compose` scope.\nDownload them to your device, and select the file.").grid(row=1, column=0)
		ttk.Button(self, text="Guide", command=self.open_guide).grid(row=2, column=0)
		ttk.Button(self, text="Select File", command=self.choose_path).grid(row=2, column=1)
		ttk.Button(self, text="Cancel", command=self.destroy).grid(row=2, column=2)
		
		self.selected_path = None
	
	def open_guide(self):
		webbrowser.open_new('https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment')
	
	def choose_path(self):
		"""Prompts the user to select the creds file."""
		self.selected_path = filedialog.askopenfilename(title="Select credentials file", filetypes=[("Google API credentials files", ".json")])
		if not (self.selected_path == None or self.selected_path == ''):
			self.destroy()
	
	def show(self):
		"""Shows the window and returns the selected file path"""
		self.deiconify()
		self.wm_protocol("WM_DELETE_WINDOW", self.destroy)
		self.wait_window(self)
		return self.selected_path


def get_creds(token_path, creds_path, root=None):
	"""Gets the user's Gmail credentials, asking for input on the command line where necessary if `prompt` is `True`."""
	creds = gmail.get_token(token_path)
	# If there are no (valid) credentials available and `prompt` is `True`, let the user log in.
	if root and (not creds or not creds.valid):
		# Create new creds
		# If OAuth2 creds do not exist, tell the user to create them
		if not os.path.exists(creds_path):
			popup = CredsPopup(root)
			creds_path_input = popup.show()
			flow = gmail.get_oauth_flow(creds_path, creds_path_input)
		else:
			flow = gmail.get_oauth_flow(creds_path)
		creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		gmail.write_token(creds, token_path)
		# Refocus the main window
		root.parent.focus_force()
	return creds
