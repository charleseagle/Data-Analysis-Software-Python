# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)
from datalabelframe import *;

from Tkinter import *

class FrameTabs(DataLabelFrame):	
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self, master=None, tabarrange="Horizontal",framename=None):
		DataLabelFrame.__dict__['__init__'](self,master,framename);
		self.pack(fill=BOTH,expand=1);
		
		self['activeframe'] = None
		self['count'] = 0
		self['buttonlist']=[];
		self['screenlist']=[];
		self['valuelist']=[];
		
		# allows the TOP and BOTTOM
		# radiobuttons' positioning.
		if tabarrange in ("Horizontal", "H"):
			self['buttonside'] = TOP;
			self['buttonarrange'] = LEFT;
		else:
			self['buttonside'] = LEFT;
			self['buttonarrange'] = TOP;
			
	# creates notebook's frames structure
		self['buttonframe'] = Frame(self, borderwidth=2, relief=SUNKEN)
		self['buttonframe'].pack(side=self['buttonside'],fill=X)
		#self['screenframe'] = Frame(self, borderwidth=2, relief=RIDGE)
		#self['screenframe'].pack(fill=BOTH,expand=1)
		self['choice'] = IntVar(self);
		
	# return a master frame reference for the external frames (screens)
	#def __call__(self):
	#	return self['screenframe'];
		
	# add a new frame (screen) to the (bottom/left of the) notebook
	def add_screen(self, fr, title):
		b = Radiobutton(self['buttonframe'], text=title, \
		indicatoron=0,variable=self['choice'], \
		value=self['count'], command=lambda: self.display(fr))
		b.pack(side=self['buttonarrange'],fill=BOTH)
	
		self['buttonlist'].append(b);
		self['screenlist'].append(fr);
		self['valuelist'].append(self['count']);
		
		# ensures the first frame will be
		# the first selected/enabled
		if self['activeframe'] is None:
			fr.pack(fill=BOTH, expand=1)
			self['activeframe'] = fr;
			self['choice'].set(self['count']);
		else:
			fr.forget();
		
		self['count'] += 1;
		
		# returns a reference to the newly created
        # radiobutton (allowing its configuration/destruction) 
		#self.display(fr);
		return b
	
	def del_screen(self,fr):
		I=self['screenlist'].index(fr);
		bu=self['buttonlist'].pop(I);
		sc=self['screenlist'].pop(I);
		self['valuelist'].pop(I);
		bu.destroy();
		if self['activeframe'] == fr and len(self['screenlist'])>=1:
			self.setactive(-1);
			
	def del_tab(self,tabname):
		buttonfound=self.find_tab(tabname);
		if buttonfound is not None:
			I=self['buttonlist'].index(buttonfound);
			fr=self['screenlist'][I];
			self.del_screen(fr);
	
	def find_tab(self,tabname):
		buttonfound=None;
		for button in self['buttonlist']:
			if button.cget('text')==tabname:
				buttonfound=button;
		return buttonfound;
	
	def add_tab(self,tabname,screen,overwrite=False):
		buttonfound=self.find_tab(tabname);
		if buttonfound is not None:
			if overwrite is True:
				self.del_tab(tabname);
				self.add_screen(screen,tabname);
				self.setactive(-1);
			else:
				I=I=self['buttonlist'].index(buttonfound);
				self.setactive(I);
		else:
			self.add_screen(screen,tabname);
			self.setactive(-1);	
		
	# hides the former active frame and shows 
	# another one, keeping its reference
	def display(self, fr):
		#print "choice",self['choice'],self['choice'].get()
		#print "to display frame"
		self['activeframe'].forget();
		#print "forgotten"
		fr.pack(fill=BOTH,expand=1)
		#print "packed"
		self['activeframe'] = fr;
		
	def setactive(self,index):
		if index<0:
			index=index+len(self['screenlist'])
		if index>=0:
			self.display(self['screenlist'][index]);
			self['choice'].set(self['valuelist'][index]);
			#print "setchoice"
		else:
			self['activeframe']=None;