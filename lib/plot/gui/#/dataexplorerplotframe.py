from dataexplorerframe import *;
from xpyfigure import *;

import pylab;
from Tkinter import *;

class DataExplorerPlotFrame(DataExplorerFrame):
	def __init__(self,master=None,objname=None,dataobj=None):
		#print 'type of arg datawindow', type(datawindow)
		DataExplorerFrame.__dict__['__init__'](self,master,objname,dataobj);		
		self.__ginit();
		
		if dataobj is not None:
			self.exploredata(dataobj,objname);
		
	def __ginit(self):
		#print "in DataExplorerPlotFrame ginit"
		toolbarplot=Frame(self['self']);
		toolbarplot.pack(side=LEFT,fill=BOTH);
		
		b = Button(toolbarplot, text="Plotxy", command=self.plotxy)
		b.pack(side=LEFT)
		b = Button(toolbarplot, text="Plotxyz", command=self.plotxyz)
		b.pack(side=LEFT)
		
		#self.gosub(self);	
		#self.gosub(self);
		
	def contextmenu(self,listbox):
		#menu=DataExplorerFrame.__dict__.contextmenu(self,event,listbox);
		menu=DataExplorerFrame.__dict__['contextmenu'](self,listbox);
		menu.add_separator();
		menu.add_command(label="plotxy", command=self.plotxy)
	
	def getxyplotstyle(self):
		controlwin=self.getrootdatawin();
		xycfg=controlwin.getxyplotstyle();
		return xycfg;
		
	def getfigcfg(self):
		controlwin=self.getrootdatawin();
		figcfg=controlwin.getfigcfg();
		return figcfg;
		
	def plotxy(self):
		import time;
		t0=time.time();
		self.setfig2plot();
		datalist=self.getcurrentdatalist();
		datanamelist=self.getcurrentdatanamelist();
		xycfg=self.getxyplotstyle();
		xycfg['labels']=True;
		i=0;
		pylab.ioff();
		for i in range(len(datalist)):
			data=datalist[i];
			dataname=datanamelist[i];
			xycfg['linename']=dataname;
			self.plotxysingle(data,xycfg);
			xycfg.nextplotstyle();
			if i==0:
				pylab.hold(True);
			else:
				xycfg['labels']=None;
			i=i+1;
			#print "i=",i
		pylab.ion();
		self.setgrid();	
		print "Time taken to plot:",time.time()-t0;
		
	def plotxysingle(self,data,plotstyle):
		h=None;
		#print 'xycfg:',xycfg;
		try:
			h=data.plot(plotstyle);
			#print "h1"
			fig=pylab.gcf();
			#print "fig1"
			xfig=XpyFigure(fig.number);
			#print "xfig1",xfig,type(xfig);
			#xfig.add_plotable(data);
			#print "add1"
		except:
			try:
				h=data.plot();
				#print "h"
				fig=pylab.gcf();
				#print "fig"
				xfig=XpyFigure(fig.number);
				#print "xfig1",xfig,type(xfig);
				xfig.add_plotable(data);
				#print "add"
			except:
				#print 'Not an xyplotable object, try list';
				try:
					#print xycfg['linecfg']
					h=pylab.plot(data,plotstyle.getplotstyle());
					
				except:
					import tkMessageBox;
					tkMessageBox.showerror('Erorr in plotdata','None plotable data!');
		#print "h type:",type(h);
		if h is not None:
			#print "set line and marker"
			pylab.setp(h,linewidth=plotstyle['linewidth']);
			pylab.setp(h,markersize=plotstyle['markersize']);
		
		
	def plotxyz(self):
		print "plotting xyz"
		
	def setfig2plot(self):
		#xfig=XpyFigure();
		#ax=pylab.gca();
		figcfg=self.getfigcfg();
		#print "figcfg:",figcfg;
		if figcfg['newfig']==1:
			xfig=XpyFigure();
		if figcfg['hold']==1:
			pylab.hold(True);
		else:
			pylab.hold(False);
	
	def setgrid(self):		
		ax=pylab.gca();
		figcfg=self.getfigcfg();
		if figcfg['grid']==1:
			pylab.grid(True);
		else:
			pylab.grid(False);