# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)

from Tkinter import *
from dataobject import *;
from datawidget import *;

class DataLabelFrame(DataWidget,LabelFrame):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self, master=None,framename=None):
		LabelFrame.__dict__['__init__'](self,master,text=framename);
		#self.pack();
		self['self']=self;
		

	def quit(self):
		children=self.winfo_children();
		#print len(children),type(children)
		for c in children:
			#print "type",type(c)
			self.delchild(c);
		parent=self.master;
		#if isa(parent,'FrameTabs','frametabs'):
		#	#print "found frame"
		#	parent.del_screen(self);
		
		#print (parent);
		#print dir(parent.master)
		#curpage=parent.master.getcurselection();
		#parent.delete(curpage);
		
		#print "erro deleting"
		#pass;
		self.gcdestroy();
		
	def delchild(self,child):
		#print "in delchild"
		#print "type",type(child)
		grandchildren=child.winfo_children();
		if grandchildren is not None:
			for g in grandchildren:
				self.delchild(g);
		try:
			child.gcdestroy();
		except:
			child.destroy();
		
	def gcdestroy(self):
		self.cleardata();
		self.destroy();