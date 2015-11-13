from controlframe import *;

from Tkinter import *;

class TextOutFrame(ControlFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		ControlFrame.__dict__['__init__'](self,master,framename=framename);	
		self['textoutlist']=[];
		self.__ginit();
	
	def __ginit(self):
		toolbar=self['toolbar'];
		
		b = Button(toolbar, text="Refresh", command=self.refresh)
		b.pack(side=LEFT);
		b = Button(toolbar, text="Clear", command=self.clear)
		b.pack(side=LEFT);
		#print self.keys()
		#print "type",type(self)
		txtoutframe=Frame(self['self']);
		txtoutframe.pack(fill=BOTH,expand=1);
		scrollbar=Scrollbar(txtoutframe);
		scrollbar.pack(side=RIGHT,fill=BOTH,);
		
		txt=Text(txtoutframe,yscrollcommand=scrollbar.set,width=50);
		self['textouttext']=txt;
		txt.pack(side=LEFT,fill=BOTH,expand=1);
		scrollbar.config(command=txt.yview)

		
	def	refresh(self):
		self['textouttext'].delete(1.0, END);
		for l in self['textoutlist']:
			self['textouttext'].insert(END,str(l));
			self['textouttext'].insert(END,'\n');
		self['textouttext'].update();
		
	def print_(self,text):
		self['textoutlist'].append(text);
		self['textouttext'].insert(END,text);
		self['textouttext'].insert(END,'\n');
		self['textouttext'].yview_moveto(1);
		self['textouttext'].update();
		#print "updated"
	
	def clear(self):
		self['textoutlist']=[];
		self.refresh();