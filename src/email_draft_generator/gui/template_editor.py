import os
import json
import pathlib
import json_fix
import subprocess
import platform

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from email_draft_generator.attachment import EmailAttachment
from email_draft_generator.gui import util
from email_draft_generator.email_template import EmailTemplate


class AttachmentEditorPopup(tk.Toplevel):
	"""An editor window for EmailAttachments."""
	
	def __init__(self, parent, attachment: EmailAttachment):
		super().__init__(parent)
		# TODO: Add a file preview?
		
		self.wm_title("Attachment Editor: " + attachment.filename)
		
		# Allow the contents to expand to the size of the frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		self.attachment = attachment
		self.deleted = False
		
		# Filename
		filename_frame = tk.LabelFrame(self, text="File Name", padx=5, pady=5)
		filename_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		filename_frame.grid_rowconfigure(0, weight=1)
		filename_frame.grid_columnconfigure(0, weight=1)
		
		self.filename_textbox = util.SettableEntry(filename_frame)
		self.filename_textbox.grid(sticky="nsew")
		self.filename_textbox.set_text(self.attachment.filename)
		
		buttons_frame = ttk.Frame(self)
		buttons_frame.grid(row=1, column=0, sticky="ew")
		ttk.Button(buttons_frame, text="Preview", command=self.open).grid(row=0, column=0)
		ttk.Button(buttons_frame, text="Delete", command=self.delete).grid(row=0, column=1)
		ttk.Button(buttons_frame, text="Close", command=self.destroy).grid(row=0, column=2)
	
	def open(self):
		if platform.system() == 'Darwin':  # macOS
			subprocess.call(('open', self.attachment.path))  # type: ignore
		elif platform.system() == 'Windows':  # Windows
			os.startfile(self.attachment.path)  # type: ignore
		else:  # linux variants
			subprocess.call(('xdg-open', self.attachment.path))  # type: ignore
	
	def delete(self):
		self.deleted = True
		self.destroy()
	
	def show(self):
		"""Shows the window and returns the template."""
		self.deiconify()
		self.wait_window()
		# TODO: Figure out why this doesnt work
		#self.attachment.filename = self.filename_textbox.get()
		if not self.deleted:
			return self.attachment
		else:
			return False


class AttachmentEditor(tk.Frame):
	"""An editor for a template's EmailAttachments."""
	
	def __init__(self, parent):
		super().__init__(parent)
		
		# Frame to contain attachments
		self.attachment_frame = tk.LabelFrame(self, text="Attachments", padx=5, pady=5)
		self.attachment_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
		
		self.attachment_frame.grid_rowconfigure(0, weight=1)
		self.attachment_frame.grid_columnconfigure(0, weight=1)
		
		ttk.Button(self, text="New Attachment", command=self.new).grid(row=1, column=0)
	
	def new(self):
		attachment_path = filedialog.askopenfilename()
		self.attachments.append(EmailAttachment.from_path(pathlib.Path(attachment_path)))
		self.set_attachments(self.attachments)
	
	def set_attachments(self, attachments):
		self.attachments = attachments
		# Remove all of the previous attachments fromt the frame
		for widget in self.attachment_frame.winfo_children():
			widget.destroy()
		# Add a widget for each attachment
		for i, attachment in enumerate(attachments):
			button = ttk.Button(self.attachment_frame, text=attachment.filename, command=lambda: self.edit_attachment(i))
			button.grid(row=0, column=i)
	
	def edit_attachment(self, attachment: int):
		editor = AttachmentEditorPopup(self, self.attachments[attachment])
		self.attachments[attachment] = editor.show()
		if self.attachments[attachment] == False:
			self.attachments.pop(attachment)
		self.set_attachments(self.attachments)
	
	def get(self):
		return self.attachments


class TemplateEditor(tk.Frame):
	"""An editor for EmailTemplates."""
	
	def __init__(self, parent, template: EmailTemplate | None = None):
		super().__init__(parent)
		
		if template == None:
			self.template = EmailTemplate.get_sample_template()
		else:
			self.template = template
		
		# Subject
		subject_frame = tk.LabelFrame(self, text="Subject", padx=5, pady=5)
		subject_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		subject_frame.grid_rowconfigure(0, weight=1)
		subject_frame.grid_columnconfigure(0, weight=1)
		
		self.subject_textbox = util.SettableEntry(subject_frame)
		self.subject_textbox.grid(sticky="nsew")
		
		# Body
		body_frame = tk.LabelFrame(self, text="Body", padx=5, pady=5)
		body_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
		body_frame.grid_rowconfigure(0, weight=1)
		body_frame.grid_columnconfigure(0, weight=1)
		
		self.body_textbox = util.SettableScrolledText(body_frame)
		self.body_textbox.grid(sticky="nsew")
		
		# Attachments
		self.attachment_editor = AttachmentEditor(self)
		self.attachment_editor.grid(sticky="nsew")
		
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=0)
		self.grid_columnconfigure(0, weight=1)
		
		self.set_template(self.template)
	
	def get_template(self):
		"""Returns the current template."""
		return EmailTemplate(subject=self.subject_textbox.get(), body=self.body_textbox.get("1.0", "end-1c"), attachments=self.attachment_editor.get())
	
	def set_template(self, template: EmailTemplate):
		"""Sets the template."""
		self.subject_textbox.set_text(template.subject)
		self.body_textbox.set_text(template.body)
		self.attachment_editor.set_attachments(template.attachments)
		self.template = template
	
	def check_if_edited(self):
		"""Compares the current template to the saved data."""
		return self.template != self.get_template()


class TemplateEditorWindow(tk.Frame):
	"""An editor for EmailTemplates with an interface to control it."""
	
	def __init__(self, parent, template: EmailTemplate | None = None, *, popup=False):
		super().__init__(parent, padx=10, pady=10)
		self.parent = parent
		self.popup = popup
		
		self.parent.wm_title("Template Editor")
		self.parent.wm_protocol("WM_DELETE_WINDOW", self.quit_with_prompt)  # Prompt to save on quit
		
		# Allow the contents to expand to the size of the frame
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid(sticky="nsew")
		
		# Buttons
		buttons_frame = ttk.Frame(self)
		buttons_frame.grid(row=0, column=0, sticky="ew")
		
		if popup:
			ttk.Button(buttons_frame, text="Save and Return", command=self.save_template).grid(row=0, column=0)
			ttk.Button(buttons_frame, text="Save As...", command=self.save_template_as).grid(row=0, column=1)
			ttk.Button(buttons_frame, text="Cancel", command=self.quit_with_prompt).grid(row=0, column=2)
		else:
			ttk.Button(buttons_frame, text="Open", command=self.load_template).grid(row=0, column=0)
			ttk.Button(buttons_frame, text="Save", command=self.save_template).grid(row=0, column=1)
			ttk.Button(buttons_frame, text="Save As...", command=self.save_template_as).grid(row=0, column=2)
			ttk.Button(buttons_frame, text="Exit", command=self.quit_with_prompt).grid(row=0, column=3)
		
		self.template_editor = TemplateEditor(self, template)
		self.template_editor.grid(row=1, column=0, sticky="nsew")
	
	def prompt_to_save(self):
		"""Prompt the user to save if the file has been edited.
		
		Return:
			`True` if user selected `Yes` or `No` or the file has not been edited, `False` if user selected `Cancel`.
		"""
		if self.template_editor.check_if_edited():
			save_prompt = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Would you like to save them?")
			if save_prompt == True:
				self.save_template()
			elif save_prompt == False:
				self.template_editor.set_template(self.template_editor.template)
			
			return save_prompt != None
		else:
			return True
	
	def load_template(self):
		"""Prompts the user to select the template file."""
		if self.prompt_to_save():
			self.template_path = filedialog.askopenfilename(title="Select E-mail template", filetypes=[("E-mail template files", ".json")])
			
			if self.template_path == None or self.template_path == '':
				return
			
			# Parse template
			with open(self.template_path) as template_file:
				try:
					self.template_editor.set_template(EmailTemplate.from_file(template_file))
				except Exception as ex:
					messagebox.showerror(message=str(ex))
			
			self.parent.wm_title("Template Editor - " + os.path.basename(self.template_path))
	
	def save_template(self):
		"""Saves the current template and returns to the main window if it is a popup."""
		self.template_editor.template = self.template_editor.get_template()
		
		if not hasattr(self, "template_path"):
			# If no template file was opened, prompt the user to save to a new file
			template_path = filedialog.asksaveasfilename(title="Select where to save the template", defaultextension=".json")
			if template_path == None or template_path == '':
				if self.popup:
					self.parent.withdraw()
				return
			else:
				self.template_path = template_path
				self.parent.wm_title("Template Editor - " + os.path.basename(self.template_path))
		
		with open(self.template_path, "w") as template_file:
			json.dump(self.template_editor.template, template_file)
		
		if self.popup:
			self.parent.withdraw()
	
	def save_template_as(self):
		"""Saves the current template as a new file."""
		self.template_editor.template = self.template_editor.get_template()
		
		template_path = filedialog.asksaveasfilename(title="Select where to save the template", defaultextension=".json")
		if template_path == None or template_path == '':
			return
		else:
			self.template_path = template_path
			self.parent.wm_title("Template Editor - " + os.path.basename(self.template_path))
		
		self.save_template()
	
	def quit_with_prompt(self):
		"""Quit, prompting the user to save if the file has been edited."""
		if self.prompt_to_save():
			# If the window is a popup, hide it so it can be used again later
			if self.popup:
				self.parent.withdraw()
			else:
				self.parent.destroy()


class TemplateEditorPopup(tk.Toplevel):
	
	def __init__(self, parent, template: EmailTemplate | None = None):
		super().__init__(parent)
		# Allow the contents to expand to the size of the frame
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		# Template Editor
		self.template_editor = TemplateEditorWindow(self, template, popup=True)
		self.template_editor.grid(row=0, column=0, sticky="nsew")
	
	def show(self):
		"""Shows the window and returns the template."""
		self.deiconify()
		self.wait_visibility()
		return self.template_editor.template_editor.template


def main():
	root = tk.Tk()
	editor = TemplateEditorWindow(root)
	editor.pack(expand=True, fill='both')
	editor.mainloop()
