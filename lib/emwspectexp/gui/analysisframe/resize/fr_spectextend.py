from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;

class Fr_SpectExtend(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):
		self.gettmpdata('savename').set('extened');
		self.ginitsourcedataentry('sourcedata');
		
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		fullfilechosen=easygui.fileopenbox('Please choose a file (Ref for opus) to open','Opeing a file...',"*");
		if fullfilechosen is not None:
			extstandard=EMWSpectrum(fullfilechosen);
			extstandard.import_();
			extstandard['xunit'].setcurrentunit("cm_1");
			spectra.plot();
			extstandard.plot();

			for k in spectra.keys():
				self.getrootdatawin().print_(("k:",k));
				spect=spectra[k];
				spectnew=spect.copyxy();
				spectnew.extend(extstandard,smooth=1);
				spectnew.log({"Operation":"extend","extstandard":fullfilechosen,"smooth":1});
				spectranew.insert(spectnew,k);
					
				database[0]['resultdatatablegroups'][igroup]=spectranew;
			spectranew.plot('o');
			