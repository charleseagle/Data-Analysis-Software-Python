from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;
from tmp_pickrange import *;

class Fr_SpectSmooth(DataOperationFrame,Tmp_PickRange):
	def __init__(self,master=None,framename=None):
		#print 'type of arg datawindow', type(datawindow)
		DataOperationFrame.__dict__['__init__'](self,master,framename=framename);	
		self.__ginit();
		Tmp_PickRange.ginit(self);
		
	def __ginit(self):		
		self.gettmpdata('savename').set('smoothed');
		#for i in range(self['numofsourcedatabase']):
		self.ginitsourcedataentry('spectra2smooth');		
		parameterframe=self['parameterframe'];
		
		parameterframe=self['parameterframe'];
		self['width']=StringVar();
		self['width'].set("0.001");
		self['chkbase'] = IntVar();
		self['chkedge'] = IntVar();
		
		l=Label(parameterframe, text="width factor");
		l.pack(side=TOP);
		e=Entry(parameterframe, textvariable=self['width']);
		e.pack();
		
		c=Checkbutton(parameterframe, text="Base line ?", variable=self['chkbase'])
		c.pack();
		c= Checkbutton(parameterframe, text="Conserve edge?", variable=self['chkedge'])
		c.pack();
		
		self.gettmpdata("groupstr").set("'min(x)','max(x)'");
			
	def analyze(self,igroup):
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		
		spectranew=spectra.getemptyinstance();
		spectra.plot();
		
		xmin=float(self['xminstr'].get());
		xmax=float(self['xmaxstr'].get());

		for k in spectra.keys():
			spect=spectra[k];
			spectnew=spect.copyxy();
			widthfactor=float(self['width'].get());
			#print "widthfactor:",widthfactor
			base=self['chkbase'].get();
			edgeconserve=self['chkedge'].get();
			xwidth=(xmax-xmin)*widthfactor;
			spectnew.smooth(xwidth,xmin=xmin,xmax=xmax,base=base,edgeconserve=edgeconserve);
			spectnew.log({"Operation":"smooth","xwidth":xwidth,"xmin":xmin,"xmax":xmax,"base":base,"edgeconserve":edgeconserve});
			#print "spectranew type after:", type(spectranew);
			spectranew.insert(spectnew,k);
				
		database[0]['resultdatatablegroups'][igroup]=spectranew;
		spectranew.plot('o');
		#pass;
		

