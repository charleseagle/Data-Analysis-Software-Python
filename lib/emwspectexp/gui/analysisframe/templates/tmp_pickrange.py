from Tkinter import *;
from dataobject import *;
from dataoperationframe import *;
import easygui;
import pylab;

class Tmp_PickRange(DataObject):
	def __init__(self):
		#print 'type of arg datawindow', type(datawindow)
		pass;
		
	def ginit(self):
		self['xminstr']=StringVar();
		self['xminstr'].set('0')
		self['xmaxstr']=StringVar();
		self["xmaxstr"].set('1e5');
		
		parameterframe=self['parameterframe'];
		rangeframe=LabelFrame(parameterframe,text="x Range");
		rangeframe.pack(side=LEFT);
		
		lmin=Label(rangeframe, text="xmin");
		#lmin.pack(side=TOP);
		emin=Entry(rangeframe, textvariable=self['xminstr'],width=20);
		#emin.pack();
		lmax=Label(rangeframe, text="xmax");
		#lmax.pack(side=TOP);
		emax=Entry(rangeframe, textvariable=self['xmaxstr'],width=20);
		#emax.pack();
		lmin.grid(row=0,column=0);
		emin.grid(row=0,column=1);
		lmax.grid(row=1,column=0);
		emax.grid(row=1,column=1);
		b=Button(rangeframe,text="Choose range",command=self.setrange);
		b.grid(row=2,column=0);
		b=Button(rangeframe,text="Select all",command=self.allrange);
		b.grid(row=2,column=1);
		
	def setrange(self):
		igroup=self.gettmpdata('groupnum').get();
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		spectra.plot();
		#print "spectranew type:",type(spectranew);
		
		answer=easygui.boolbox("Choose the range for group "+str(igroup),"picking spectra part",["OK","Cancel"]);
		if answer==1:
			A=pylab.axis();
			xmin=A[0];
			xmax=A[1];
			self['xminstr'].set(str(xmin));
			self['xmaxstr'].set(str(xmax));
	
	def allrange(self):
		igroup=self.gettmpdata('groupnum').get();
		database=self.gettmpdata('database');
		spectra=database[0]['resultdatatablegroups'][igroup];
		spectranew=spectra.getemptyinstance();
		#print "spectranew type:",type(spectranew);
		keys=spectra.keys();
		xmin=min(spectra[keys[0]]['x']);
		xmax=max(spectra[keys[0]]['x']);
		
		for k in keys:
			xmin=min(xmin,min(spectra[k]['x']));
			xmax=max(xmax,max(spectra[k]['x']));
			self.stdout( (xmin,xmax));
		self['xminstr'].set(str(xmin));
		self['xmaxstr'].set(str(xmax));