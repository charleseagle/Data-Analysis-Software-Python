from datalabelframe import *;
from xyplotstyle import *;

from Tkinter import *;

class XyzPlotControlFrame(DataLabelFrame):
	def __init__(self,master=None):
		DataLabelFrame.__dict__['__init__'](self, master)
		self['master']=master;
		
		self['xyzstylelist']=['image','contour','xy lines'];		
		
		self['optxyzstyle']=StringVar();
		self['chktranspose']=IntVar();
		
		self['strvmin']=StringVar();
		self['strvmin'].set('');
		self['strvmax']=StringVar();
		self['strvmax'].set('');		
		self['chkvmin'] = IntVar();
		self['chkvmin'].set(0);
		self['chkvmax'] = IntVar();
		self['chkvmax'].set(0);
		
		self.__ginit();
		
	def __ginit(self):
		#frames for line and marker
		self['xyzframe'] = LabelFrame(self,text='xyz property');
		self['xyzframe'].pack(fill=BOTH)		
		
		#xyz properties
		optxyzstyle = apply(OptionMenu,(self['xyzframe'],self['optxyzstyle']) + tuple(self['xyzstylelist']));
		self['optxyzstyle'].set(self['xyzstylelist'][0]);
		chktranspose=Checkbutton(self['xyzframe'], text="Transpose", variable=self['chktranspose']);
		labxyzstyle=Label(self['xyzframe'],text='Style');
		#labtranspose=Label(self['xyzframe'],text='Transpose');
		
		labxyzstyle.grid(row=0,column=0,sticky=W);
		#labtranspose.grid(row=1,column=0,sticky=W);
		chktranspose.grid(row=1,column=1,columnspan=2,sticky=W);
		optxyzstyle.grid(row=0,column=1,sticky=W);
		
		#labvmin = Label(self['xyzframe'], text="vmin");
		#labvmax = Label(self['xyzframe'], text="vmin");
		evmin = Entry(self['xyzframe'],textvariable=self['strvmin'],width=10);
		evmax = Entry(self['xyzframe'],textvariable=self['strvmax'],width=10);
		chkvmin = Checkbutton(self['xyzframe'], text="vmin?", variable=self['chkvmin']);
		chkvmax = Checkbutton(self['xyzframe'], text="vmax?", variable=self['chkvmax']);
		
		chkvmin.grid(row=2,column=0,columnspan=1,sticky=W);
		evmin.grid(row=2,column=1,columnspan=2,sticky=W);
		chkvmax.grid(row=3,column=0,columnspan=1,sticky=W);
		evmax.grid(row=3,column=1,columnspan=2,sticky=W);
		#chkvmin.pack(side=LEFT);
		#evmin.pack(side=RIGHT);
		#chkvmax.pack(side=LEFT);
		#evmax.pack(side=RIGHT);
		
		"""
		chkhold = Checkbutton(self, text="Hold on?", variable=self['chkhold'])
		chknewfig = Checkbutton(self, text="New figure?", variable=self['chknewfig'])
		chkgrid = Checkbutton(self, text="Grid?", variable=self['chkgrid'])
		
		optmarker.grid(row=0,column=0,columnspan=2,sticky=W+E);
		optcolor.grid(row=1,column=0,columnspan=1,sticky=W+E);
		optlineshape.grid(row=2,column=0,columnspan=1,sticky=W+E);
		
		chkhold.grid(row=0,column=5,columnspan=2,sticky=W);
		chknewfig.grid(row=1,column=5,columnspan=2,sticky=W);
		chkgrid.grid(row=2,column=5,columnspan=2,sticky=W);
		#sbcolor.pack(side=BOTTOM, fill=BOTH);
		"""
		
		
	def getvmin(self):
		vmin=None;
		if self['chkvmin'].get()==1:
			vmin=eval(self['strvmin'].get());
		return vmin;
		
	def getvmax(self):
		vmax=None;
		if self['chkvmax'].get()==1:
			vmax=eval(self['strvmax'].get());
		return vmax;

		#def getvmax(self):
	#	return eval(self['strvmax'].get());
		
	def getcfg(self):
		#cfg={};
		cfg=XyPlotStyle();
		cfg['vmin']=self.getvmin();
		cfg['vmax']=self.getvmax();
		#print "plotstylestr:",cfg.getplotstyle();
		return cfg;