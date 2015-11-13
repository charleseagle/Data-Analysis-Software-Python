from approotwin import *; 
from controlframe import *;
from xyplotcontrolframe import *;
from xyzplotcontrolframe import *
from figurecontrolframe import *
from datalistframe import *;

import Tkinter;
import Pmw;

class PlotControlFrame(ControlFrame):
	def __init__(self,master,framename=None):
		ControlFrame.__dict__['__init__'](self,master,framename);
		self.__ginit();
		
	def __ginit(self):
		figframe=FigureControlFrame(self['self']);
		
		notebook=Pmw.NoteBook(self['self']);
		
		page=notebook.add("XyPlot");
		xyframe=XyPlotControlFrame(page);
		xyframe.pack(fill=BOTH,expand=1);
		
		page=notebook.add("XyzPlot");
		xyzframe=XyzPlotControlFrame(page);
		xyzframe.pack(fill=BOTH,expand=1);
		
		plotablelist=DataListFrame(self['self']);
		
		#plotablelist.grid(row=0,column=0,rowspan=2,sticky=W);
		#figframe.grid(row=0,column=1,sticky=W);
		#notebook.grid(row=1,column=1,sticky=W);
		notebook.setnaturalsize();
		
		plotablelist.pack(side=BOTTOM,fill=BOTH);
		notebook.pack(side=RIGHT,fill=BOTH);
		figframe.pack(side=LEFT,fill=BOTH);
		
		
		self['xycontrol']=xyframe;
		self['xyzcontrol']=xyzframe;
		self['figcontrol']=figframe;
		self['plotablelist']=plotablelist;
		
		self.addbutton(self.plotxy,"PlotXy");
		self.addbutton(self.plotxyz,"PlotXyz");
		b=self.addbutton(self.addfromexplorer,"Add");
		self.bindballoon(b,'Add data from current explorer to plotlist');
		#self.addbutton(self.clear,"Clear");
		
		
	def adddata(self,dataname,data):
		self['plotablelist'].addline(dataname,data);
		
	def getxyplotstyle(self):
		return self['xycontrol'].getcfg();
		
	def clear(self):
		self['plotablelist'].clear();
		
	def plotxy(self):
		self['figcontrol'].setfig2plot();
		datalist=self['plotablelist'].getcurrentdatalist();
		datanamelist=self['plotablelist'].getcurrentdatanamelist();
		xycfg=self['xycontrol'].getcfg();
		xycfg['labels']=True;
		i=0;
		pylab.ioff();
		for i in range(len(datalist)):
			data=datalist[i];
			dataname=datanamelist[i];
			#self.stdout(dataname);
			#self.stdout(data);
			
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
		self['figcontrol'].setgrid();
		
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
		self['figcontrol'].setfig2plot();
		datalist=self['plotablelist'].getcurrentdatalist();
		datanamelist=self['plotablelist'].getcurrentdatanamelist();

		xyzcfg=self['xyzcontrol'].getcfg();
		#xycfg['labels']=True;

		datalist[0].uiconvert2xyz(plot2dtype="image",linecfg=xyzcfg);
		
	def addfromexplorer(self):
		rootwin=self.getrootdatawin();
		exp=rootwin.getcurrentdataexplorer();
		if exp is not None:
			datalist=exp.getcurrentdatalist();
			datanamelist=exp.getcurrentdatanamelist();
			datapath=exp.getcurrentdatapath();
			for i in range(len(datanamelist)):
				n=datapath+"/"+datanamelist[i]
				self.adddata(n,datalist[i]);
		

