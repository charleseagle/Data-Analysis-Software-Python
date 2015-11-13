from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;
import os;

class Fr_SpectRefRenorm(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('refrenorm');
		self.ginitsourcedataentry('sourcedata');
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		curdir=os.path.abspath(os.curdir)
		fullfilechosen=os.path.join(curdir, "calibrationfile\\RAL.HAG");
		extstandard=EMWSpectrum(fullfilechosen);
		extstandard.import_();
		extstandard['xunit'].setcurrentunit("cm_1");
		spectra.plot();
		extstandard.plot();

		for k in spectra.keys():
			self.stdout(("k:",k));
			spect=spectra[k];
			spectnew=spect.copyxy();
			spectnew.binop(extstandard,"*");
			spectnew.log({"Operation":"refnorm","ref":"calibrationfile\\RAL.HAG"});
			spectranew.insert(spectnew,k);
					
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
			