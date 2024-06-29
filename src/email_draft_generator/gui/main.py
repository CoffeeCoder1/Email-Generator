import fileinput
import json
import os

import tkinter as tk
from tkinter import ttk

from email_draft_generator.gui import gmail_gui
from email_draft_generator.email_drafter import EmailDrafter
from email_draft_generator.email_template import EmailTemplate
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
		
		# Frame for the main app content
		frm = self
		frm.grid()
		
		# Create a template editor and hide it
		self.template_editor = TemplateEditorPopup(self)
		self.template_editor.withdraw()
		
		ttk.Button(frm, text="Authenticate", command=self.authenticate).grid(column=0, row=0)
		
		ttk.Label(frm, text="Template").grid(column=0, row=1)
		ttk.Button(frm, text="Open", command=self.template_editor.template_editor.load_template).grid(column=1, row=1)
		ttk.Button(frm, text="Edit", command=self.edit_template).grid(column=2, row=1)
		
		ttk.Button(frm, text="Draft E-mails", command=self.send_emails).grid(column=0, row=2)
	
	def authenticate(self):
		self.creds = gmail_gui.get_creds(global_token_path, global_creds_path, root=self)
	
	def edit_template(self):
		"""Opens the template editor"""
		self.template_editor.show()
		# TODO: Fix the thing where the parent window is focused on return
		#self.parent.deiconify()
	
	def send_emails(self):
		# If not authenticated, prompt the user to authenticate
		if not self.creds.valid:
			self.authenticate()
		
		#drafting_progressbar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate')
		#drafting_progressbar.grid(column=0, row=2)
		
		# TODO: Add a GUI to select and edit this
		json_data = ""
		for line in fileinput.input():
			json_data += line
		recipients = json.loads(json_data)
		#drafting_progressbar.step()
		
		# TODO: Make the progressbar work
		#drafting_progressbar.start()
		EmailDrafter.generate_drafts(recipients, self.template_editor.template_editor.template_editor.template, self.creds)
		#drafting_progressbar.stop()


def main():
	"""Tcl/Tk based GUI for email-draft-generator"""
	root = tk.Tk()
	root.title("E-mail Generator")
	root.resizable(False, False)
	app = App(root)
	app.mainloop()
