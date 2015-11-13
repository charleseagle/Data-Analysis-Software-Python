from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Tmp_InternalStandard(DataObject):
	def __init__(self):
		#print 'type of arg datawindow', type(datawindow)
		pass;
		
	def ginit(self):
		self['nameofintstandard']=StringVar();
		self['nameofintstandard'].set('');
		
		parameterframe=self['parameterframe'];
		rangeframe=LabelFrame(parameterframe,text="Internal standard");
		rangeframe.pack(side=LEFT);
		
		lstandard=Label(rangeframe, text="Name of standard spect");
		estandard=Entry(rangeframe, textvariable=self['nameofintstandard']);
		#emin.pack();
		lstandard.grid(row=0,column=0);
		estandard.grid(row=1,column=0);
		b=Button(rangeframe,text="Choose",command=self.chooseintstandard);
		b.grid(row=2,column=0);
		
	def chooseintstandard(self):
		igroup=self.gettmpdata('groupnum').get();
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		keys=spectra.keys();
		
		answer=easygui.choicebox("Choose the standard for "+str(igroup),"Choosing standard",keys);
		if answer is not None:
			self['nameofintstandard'].set(answer);