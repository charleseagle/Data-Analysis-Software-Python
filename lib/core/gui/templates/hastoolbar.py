from dataobject import *;
from Tkinter import *

class HasToolBar(DataObject):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self):
		pass;

	def toolbar_ginit(self,master):
		toolbar = Frame(master,bd=0);
		self['toolbar']=toolbar;
		toolbar.pack(side=TOP, fill=BOTH);

	def addbutton(self,command,text=None,imagefname=None):
		toolbar=self['toolbar'];
		try:
			iconexplore=self.loadimage(imagefname);
			b = Button(toolbar, image=iconexplore, command=command);
			b.photo=iconexplore;
		except:
			#text1='1'
			b = Button(master=toolbar, text=text,command=command);
		b.pack(side=LEFT);
		return b;