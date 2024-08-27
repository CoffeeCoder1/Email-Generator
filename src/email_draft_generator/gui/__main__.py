import multiprocessing
from email_draft_generator.gui import main

if __name__ == "__main__":
	# Pyinstaller fix - fixes a problem where multiprocessing will cause multiple instances of the program to spawn
	multiprocessing.freeze_support()
	
	main.main()
