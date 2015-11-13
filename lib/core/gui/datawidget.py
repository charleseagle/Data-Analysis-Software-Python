# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)

from Tkinter import *
from dataobject import *;

class DataWidget(DataObject):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self):
		pass;
		
	def gettoplevel(self):
		if isinstance(self,Toplevel):
			return self;
		this=self;
		master=this.master;
		if master is None:
			master=this;
		#print type(master)
		#print "master top",isinstance(master,Toplevel)
		#print "master tk",isinstance(master,Tk)
		while not isinstance(master,Toplevel) and not isinstance(master,Tk):
			#print type(master)
			#print master
			this=master;
			master=this.master;
			#print "master top",isinstance(master,Toplevel)
			#print "master tk",isinstance(master,Tk)
		"""
		print "top:",master.title();
		if isinstance(master,Tk):
			print "Top:",this.title();
		"""
		return 	master;
	
	def getrootdatawin(self):
		topwin=self.gettoplevel();
		return topwin.getrootdatawin();
	
	def stdout(self,msg):
		rootwin=self.getrootdatawin();
		rootwin.print_(msg);

	def bindballoon(self,widget,text):
		toplevel=self.gettoplevel();
		toplevel['balloon'].bind(widget,text);
		
	def stdoutrun(self,cmd):
		import traceback,sys;
		try:
			cmd();
		except:
			type=None
			value=None
			tb=None
			limit=None
			type, value, tb = sys.exc_info()
			body = "Traceback (innermost last):\n"
			list = traceback.format_tb(tb, limit) +            traceback.format_exception_only(type, value)
			#stack=traceback.extract_stack();
			#stack=traceback.print_exception();
			self.stdout(list);