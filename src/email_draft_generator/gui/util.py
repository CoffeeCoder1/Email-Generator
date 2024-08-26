import tkinter as tk
from tkinter import scrolledtext


class SettableText(tk.Text):
	
	def set_text(self, text):
		self.clear()
		self.insert(tk.END, text)
	
	def clear(self):
		self.delete("1.0", tk.END)


class SettableScrolledText(scrolledtext.ScrolledText):
	
	def set_text(self, text):
		self.clear()
		self.insert(tk.END, text)
	
	def clear(self):
		self.delete("1.0", tk.END)


class SettableEntry(tk.Entry):
	
	def set_text(self, text):
		self.clear()
		self.insert(0, text)
	
	def clear(self):
		self.delete(0, tk.END)
