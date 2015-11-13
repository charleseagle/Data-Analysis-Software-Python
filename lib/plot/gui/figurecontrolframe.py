from datalabelframe import *;
from xpyfigure import *;

from Tkinter import *;
import pylab;

class FigureControlFrame(DataLabelFrame):
	def __init__(self,master=None):
		DataLabelFrame.__dict__['__init__'](self, master)
		self['master']=master;
		
		self['chkhold'] = IntVar();
		self['chknewfig'] = IntVar();
		self['chkgrid'] = IntVar();	
		self['chkgrid'].set(1);
		
		self.__ginit();
		
	def __ginit(self):
		#frames for line and marker
		self['figframe'] = LabelFrame(self,text='Plot property');
		self['figframe'].pack(padx=0, pady=0,fill=BOTH)		
		
		chkhold = Checkbutton(self['figframe'], text="Hold on?", variable=self['chkhold'])
		chknewfig = Checkbutton(self['figframe'], text="Plot in new figure?", variable=self['chknewfig'])
		chkgrid = Checkbutton(self['figframe'], text="Grid?", variable=self['chkgrid'])
		
		chkhold.grid(row=0,column=0,sticky=W);
		chknewfig.grid(row=1,column=0,sticky=W);
		chkgrid.grid(row=2,column=0,sticky=W);
		
		b=Button(self,text="New figure",command=self.newfig);
		b.pack();
		
	def getcfg(self):
		cfg={};
		cfg['hold']=self['chkhold'].get();
		cfg['newfig']=self['chknewfig'].get();
		cfg['grid']=self['chkgrid'].get();
		return cfg;
		
	def checkhold(self):	
		hold=self['chkhold'].get();
		if hold==1:
			pylab.hold(True);
		else:
			pylab.hold(False);
			
	def checkgrid(self):	
		grid=self['chkgrid'].get();
		if grid==1:
			pylab.grid(True);
		else:
			pylab.grid(False);
	
	def newfig(self):
		XpyFigure();
		
	def setgrid(self):
		ax=pylab.gca();
		figcfg=self.getcfg();
		if figcfg['grid']==1:
			pylab.grid(True);
		else:
			pylab.grid(False);
			
	def setfig2plot(self):
		#xfig=XpyFigure();
		#ax=pylab.gca();
		figcfg=self.getcfg();
		#print "figcfg:",figcfg;
		if figcfg['newfig']==1:
			xfig=XpyFigure();
		if figcfg['hold']==1:
			pylab.hold(True);
		else:
			pylab.hold(False);