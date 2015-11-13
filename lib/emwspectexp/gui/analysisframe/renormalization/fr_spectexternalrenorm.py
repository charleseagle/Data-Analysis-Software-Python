from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;
from tmp_pickrange import *;

class Fr_SpectExternalRenorm(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):		
		self.gettmpdata('savename').set('renorm_ext');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('sourcedata');
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		#parameterframe=self['parameterframe'];
		parameterframe=self['parameterframe'];
		
		self['gainorshift']=IntVar();
		r=Radiobutton(parameterframe, text="Gain", variable=self['gainorshift'],value=0);
		r.pack(anchor=W);
		r=Radiobutton(parameterframe, text="Shift", variable=self['gainorshift'],value=1);
		r.pack(anchor=W)
		r=Radiobutton(parameterframe, text="Gain+Shift", variable=self['gainorshift'],value=2);
		r.pack(anchor=W);
		r=Radiobutton(parameterframe, text="Ramp", variable=self['gainorshift'],value=3);
		r.pack(anchor=W);
		self['gainorshift'].set(0);
		


	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		fullfilechosen=easygui.fileopenbox('Please choose a file external standard','Opeing a file...',"*");
		if fullfilechosen is not None:
			spectstandard=EMWSpectrum(fullfilechosen);
			spectstandard.import_();
			
			spectstandard['xunit'].setcurrentunit("cm_1");
			spectra.plot();
			spectstandard.plot();
			xmin=float(self['xminstr'].get());
			xmax=float(self['xmaxstr'].get());
				
			for k in spectra.keys():
				self.stdout(("k:",k));
				spect=spectra[k];
				spectnew=spect.copyxy();
				spectnew.renorm(spectstandard,xmin,xmax,self['gainorshift'].get());
				spectnew.log({"Operation":"renorm","spectstandard":fullfilechosen,"xmin":xmin,"xmax":xmax,"gainorshift":self['gainorshift'].get()});
				spectranew.insert(spectnew,k);
			
			spectra=database[0]['resultdatatablegroups'][igroup]=spectranew;
			spectranew.plot('o');
				#spectra=resultdatagrouped[0]['datagroups'][igroup]=spectranew;
				#spectranew.plot();
			