from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from tmp_pickrange import *;
from tmp_internalstandard import *;

class Fr_SpectInternalRenorm(DataOperationFrame,Tmp_PickRange,Tmp_InternalStandard):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		Tmp_InternalStandard.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('renorm_int');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		parameterframe=self['parameterframe'];
		
		myframe=LabelFrame(parameterframe,text="parameters");
		myframe.pack(side=LEFT);
		
		self['gainorshift']=IntVar();
		
		r=Radiobutton(myframe, text="Gain", variable=self['gainorshift'],value=0);
		#r.pack(anchor=W);
		r.grid(row=0,column=0,sticky=W);
		r=Radiobutton(myframe, text="Shift", variable=self['gainorshift'],value=1);
		#r.pack(anchor=W)
		r.grid(row=0,column=1,sticky=W);
		r=Radiobutton(myframe, text="Gain+Shift", variable=self['gainorshift'],value=2);
		#r.pack(anchor=W);
		r.grid(row=1,column=0,sticky=W);
		r=Radiobutton(myframe, text="Ramp", variable=self['gainorshift'],value=3);
		#r.pack(anchor=W);
		r.grid(row=1,column=1,sticky=W);
		r=Radiobutton(myframe, text="Ramp+Shift", variable=self['gainorshift'],value=4);
		#r.pack(anchor=W);
		r.grid(row=2,column=0,sticky=W);
		self['gainorshift'].set(0);
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");

		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		#the real calculation
		keys=spectra.keys();
		nameofintstandard=self['nameofintstandard'].get();
		if keys.count(nameofintstandard)==0:
			nameofintstandard=keys[0];
			self['nameofintstandard'].set(keys[0]);
		selection=nameofintstandard;
		
			#print selection,type(selection)
		spectra.plot();
		pylab.grid(True);
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

			#print xmin,xmax
		spectstandard=spectra[selection];
		for k in spectra.keys():
			self.stdout(("k:",k));
			spect=spectra[k];
			spectnew=spect.copyxy();
			if selection!=k:
				spectnew.renorm(spectstandard,xmin,xmax,self['gainorshift'].get());
				spectnew.log({"Operation":"renorm","spectstandard":selection,"xmin":xmin,"xmax":xmax,"gainorshift":self['gainorshift'].get()});
				#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
					
		spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');