from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;

class Fr_SpectReshapeRenorm(DataOperationFrame):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		
	def __ginit(self):		
		self.gettmpdata('savename').set('renorm_ext');
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
			#extstandard.smooth(xwidthN=100);
			
			spectra.plot();
			extstandard.plot();
			selection=easygui.choicebox("Pick a standard","internal renormalization",spectra.keys());
			if selection is not None:
				intstandard=spectra[selection];
				spectratio=intstandard.copyxy();
				#spectratio.smooth(xwidthN=100);
				spectratio.binop(extstandard,"/");
				#spectratio['y']=1/spectratio['y'];
				spectratio.plot();
				#x=spectratio['x'];
				#spectratio.smooth((max(x)-min(x))*0.01);
				#spectratio.plot();
				for k in spectra.keys():
					self.getrootdatawin().print_(("k:",k));
					spect=spectra[k];
					spectnew=spect.copyxy();
					#spectnew.smooth(xwidthN=100);
					spectnew.binop(spectratio,"/");
					spectnew.log({"Operation":"reshapenorm","extstandard":fullfilechosen,"intstandard":selection});
					spectranew.insert(spectnew,k);
					
				database[0]['resultdatatablegroups'][igroup]=spectranew;
				spectranew.plot('o');
			