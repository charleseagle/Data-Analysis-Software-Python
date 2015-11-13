#from numdatasheet import *;
from xyplot import *;
from plotcontrol import *;
from xpyfun import *;
from xyplotstyle import *;
from xpyfigure import *;
import pylab;
import scipy

class XyzPlot(XyPlot,PlotControl):
	def __init__(self):
		pass;
	
	def interp(self):
		import time;
		t0=time.time();
		self.sortxy();
		
		x = self['x'];
		y = self['y'];
		z = self['z'];
		
		Nx=min(50,len(x));
		Ny=min(50,len(y));
		Nx=320;
		Ny=240;
		
		xl=scipy.linspace(min(x),max(x),Nx);
		yl=scipy.linspace(min(y),max(y),Ny);
		#print min(x)-min(xl),max(x)-max(xl)
		#print min(y)-min(yl),max(y)-max(yl)
		#print yl
		z0=z;
		zint=None;
		for i in range(len(y)):
			#print "i=",i
			zi=z0[i,:];
			intobj=scipy.interpolate.interp1d(x,zi);
			if zint is None:
				zint=intobj(xl);
			else:
				zint=numpy.vstack((zint,intobj(xl)));
		
		#print zint.shape
		z0=zint;
		zint=None;
		for i in range(len(xl)):
			#print "i=",i
			zi=z0[:,i];
			intobj=scipy.interpolate.interp1d(y,zi);
			#print min(y)-min(yl),max(y)-max(yl)
			if zint is None:
				zint=intobj(yl);
			else:
				zint=numpy.vstack((zint,intobj(yl)));
		zint=numpy.transpose(zint);
		self['ZI']=zint;
		stdout(("time taken:",time.time()-t0));
		save('ZI.dat',zint)
		save('x.dat',xl)
		save('y.dat',yl)
		
	def image(self,linecfg='-'):
		x = self['x'];
		y = self['y'];
		ZI = self['ZI']
		
		if isinstance(linecfg,str):
			linecfg=XyPlotStyle(linecfg);
		
		if not isinstance(linecfg,XyPlotStyle):
			linecfg=XyPlotStyle(linecfg);
		vmin=linecfg.get("vmin");
		vmax=linecfg.get("vmax");
		
		pylab.imshow(ZI,origin='lower',extent=[min(x), max(x), min(y), max(y)],aspect='auto',vmin=vmin,vmax=vmax);
		self.labels();
		
	def contour(self,linecfg='-'):
		x = self['x'];
		y = self['y'];
		ZI = self['ZI']
		pylab.contour(ZI,100,origin='lower',extent=[min(x), max(x), min(y), max(y)],aspect='auto');
		self.labels();

	def contextmenu(self,menu,dataname=''):
		import time,os;
		#menu=DataObject.__dict__['contextmenu'](self,menu);
		menu.add_separator();
		menu=PlotControl.contextmenu(self,menu);
		topwin=gettoplevelmaster(menu);
		pstyle=XyPlotStyle();
		pstyle['linename']=dataname;
		try:
			self['title']=os.path.join(topwin['savepath'],topwin['winname'])+":"+dataname+'['+time.ctime()+']';
			self['title']=self['title'].replace("\\",":")
			self['title']=self['title'].replace("_",".")
		except:
			pass;
		#menu=XyDiscreteFun.__dict__['contextmenu'](self,menu);
		
		menu.add_command(label="Image",command=lambda:self.image(pstyle));
		return menu;
