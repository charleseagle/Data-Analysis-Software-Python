# file: notebook.py
# A simple notebook-like Tkinter widget.
# Copyright 2003, Iuri Wickert (iwickert yahoo.com)

from Tkinter import *
from dataobject import *;
from datalabelframe import *;
from datamenu import *;

class DataListFrame(DataLabelFrame):
	# initialization. receives the master widget
	# reference and the notebook orientation
	def __init__(self, master=None,framename=None,selectmode=EXTENDED,width=20):
		DataLabelFrame.__dict__['__init__'](self,master,framename=framename);
		#self.pack();
		self.__ginit(selectmode,width);
		self['data']={};
		
	def __ginit(self,selectmode=EXTENDED,width=20):
		myhsbar=Scrollbar(self['self'],orient=HORIZONTAL);
		myhsbar.pack(side=BOTTOM,fill=X);
		mylistbox=Listbox(self['self'],relief=SUNKEN,selectmode=EXTENDED,width=width);
		mylistbox.pack(side=LEFT, expand=YES, fill=BOTH);
		
		myvsbar=Scrollbar(self['self']);
		myvsbar.pack(side=RIGHT,fill=Y);
		
		myvsbar.config(command=mylistbox.yview);
		myhsbar.config(command=mylistbox.xview);
		mylistbox.config(yscrollcommand=myvsbar.set,xscrollcommand=myhsbar.set);
		self['listbox']=mylistbox;
		mylistbox.bind("<Button-3>", lambda event:self.rightclicklistitem(event));
		
	def addline(self,dataname,data=None):
		self['data'][dataname]=data;
		self.refresh();
		
	def refresh(self):
		self.clear();
		for k in self['data'].keys():
			self['listbox'].insert(END,k);
		
	def clear(self):
		self['listbox'].delete(0, END);
		
	def cleardata(self):
		self['data']={};
		
	def remove(self):
		for n in self.getcurrentdatanamelist():
			del self['data'][n];
		self.refresh();
		
	
	def getcurrentselectionlist(self):
		selistrtup=self['listbox'].curselection();
		selinumlist=[];
		for k in selistrtup:
			selinumlist.append(int(k));
		return selinumlist;
	
	def getcurrentdatanamelist(self):
		datanamelist=[];
		curselilist=self.getcurrentselectionlist();	
		for i in curselilist:
			name=self['data'].keys()[i];
			datanamelist.append(name);
		return datanamelist;
		
	def getcurrentdatalist(self):
		datalist=[];
		datanamelist=self.getcurrentdatanamelist();
		for name in datanamelist:
			data=self['data'][name];
			datalist.append(data);
		return datalist;
		
	def rightclicklistitem(self,event):
		#self['currentchainindex']=ichain;
		menu = DataMenu(self);
		menu.add_command(label="Clear", command=self.clear);
		menu.add_command(label="Remove", command=self.remove);
		datalist=self.getcurrentdatalist();
		datanamelist=self.getcurrentdatanamelist();
		#print "len:",len(datalist);
		"""
		if len(datalist)==1:
			data=datalist[0];
			dataname=datanamelist[0];
			if isdatobj(data):
				menu=data.contextmenu(menu,dataname);
		"""
		menu.post(event.x_root, event.y_root)
