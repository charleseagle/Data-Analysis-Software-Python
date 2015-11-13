from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
from pylab import *;
from xpyfigure import *;
from emwspectrum import *;
from absorbanceunits import *;

class Fr_SpectAbsorption(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('absorption');
		self.ginitsourcedataentry('sourcedata');
		
		self['thickness']=StringVar();
		self['thickness'].set('1e-4')
		
		parameterframe=self['parameterframe'];
		l=Label(parameterframe, text="Sample thickness (meter)");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['thickness']);
		e.pack();

				
	def analyze(self,igroup):
		import time;
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		thickness=float(self['thickness'].get());
		#print efree,alpha,lowmethod;
		self.stdout(thickness);
		print spectra.keys();
		
		for k in spectra.keys():
			#self.getrootdatawin().stdout(("k:",k));
			#print k;
			self.stdout(k);
			t=time.time();
			self.stdout(t)
			spect=spectra[k];
			statuslabel=self.gettoplevel()['statuslabel'];
			#spectnew=spect.phaseshifts(efree,alpha,lowmethod,statuslabel);
			spectnew=spect.copyxy();
			y=spectnew['y'];
			y=-log(y)/thickness;
			spectnew['y']=y;
			spectnew['yunit']=AbsorbanceUnits();
			spectnew.log({"Operation:":"Transmittance to Absorption","thickness":thickness})
			spectranew.insert(spectnew,k);
			#spectnew.plot();
			#spectnew.show();
			#print "time taken:",time.time()-t;
			#self.stdout(("time taken:",time.time()-t));
			
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		#database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
			