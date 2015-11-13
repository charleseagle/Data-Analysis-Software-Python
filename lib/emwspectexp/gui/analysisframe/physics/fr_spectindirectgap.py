from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from xpyfigure import *;
from emwspectrum import *;
from tmp_pickrange import *;

class Fr_SpectIndirectGap(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):
		self.gettmpdata('savename').set('indirectgap');
		self.ginitsourcedataentry('Absorption coefficient');
		#self.gettmpdata("groupstr").set("'min(x)','max(x)'");
		
	def analyze(self,igroup):
		import time;
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());
		for k in spectra.keys():
			#self.getrootdatawin().stdout(("k:",k));
			#print k;
			self.stdout(k);
			spect=spectra[k];
			(gap,P,spectnew,gaperr)=spect.findindirectgap(xmin,xmax);
			x=numpy.array([gap,xmax]);
			y=numpy.polyval(P,x);
			spectnew.plot();pylab.hold("True");
			pylab.plot(x,y);
			spectnew['indirectgap']=gap;
			spectranew.insert(spectnew,k);
			spectnew['indirectgaperr']=gaperr;
			self.stdout((k,gap));
		spectgap=spectranew.uicolumn2xy(ycolumn='indirectgap');
		spectgaperr=spectranew.uicolumn2xy(ycolumn='indirectgaperr');
		spectgap.log({"method":"findindirectgap","xmin":xmin,"xmax":xmax});
		spectranew1=spectranew.getemptyinstance();
		spectranew1.insert(spectgap,'indirectgap');
		spectranew2=spectranew.getemptyinstance();
		spectranew2.insert(spectgaperr,'indirectgaperr');
		
		#database[0]['resultdatatablegroups'][igroup]=spectranew1;
		#spectranew.plot('o');
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spectranew1;
		resultdata['savestr']="value";
		database[0]=resultdata;
		
		resultdata=database[0].copy();
		resultdata['resultdatatablegroups']=database[0]['resultdatatablegroups'][:];
		resultdata['resultdatatablegroups'][igroup]=spectranew2;
		resultdata['savestr']="error";
		database.append(resultdata);			