# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)

from Tkinter import *
from dataobject import *;
from datawidget import *;

class DataMenu(Menu,DataWidget):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self, master=None,tearoff=None):
		if tearoff is None:
			tearoff=0;
		Menu.__dict__['__init__'](self,master,tearoff=tearoff);
		
	def add_command(self,label="Nolable", command=None):
		Menu.add_command(self,label=label,command=lambda: self.stdoutrun(command));
		
