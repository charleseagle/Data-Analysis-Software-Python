# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)

from Tkinter import *
from dataobject import *;

class DataMenu(DataObject,Menu):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self, master=None):
		if isinstance(master,DataMenu):
			master=master['tkmenu'];
		print "master type",type(master)
		self['tkmenu']=Menu(master,tearoff=0);
		self['submenus']={};
		
		
	def add_submenu(self,menuname):
		print "submenu name",menuname
		submenu=DataMenu(self['tkmenu']);
		self['tkmenu'].add_cascade(label=menuname,menu=submenu['tkmenu']);
		self['submenus'][menuname]=submenu;
		return submenu;
		
	def add_command(self,cmdname,cmd):
		self['tkmenu'].add_command(label=cmdname,command=cmd);