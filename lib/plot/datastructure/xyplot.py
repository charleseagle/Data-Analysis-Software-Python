#from numdatasheet import *;
from dataobject import *;
from xpyfun import *;
from xyplotstyle import *;
from xpyfigure import *;
from plotcontrol import *;
import pylab;

class XyPlot(DataObject,PlotControl):
	def __init__(self):
		pass;
		
	def plot(self,linecfg='-'):
		#x=self['x'];
		#y=self['y'];
		#xunit=self['xunit'];
		#yunit=self['yunit'];
		
		pfig=XpyFigure(pylab.gcf().number);
		if isinstance(linecfg,str):
			linecfg=XyPlotStyle(linecfg);
			
		linecfgstr=linecfg.getplotstyle();
		linename=linecfg.get('linename');
		showlabels=linecfg.get('showlabels');
		
		#print "xunit",linecfg.get("xunit")
		if linecfg.get("xunit") is not None:
			spect=self.copyxy();
			spect.convertx(linecfg.get("xunit"));
		else:
			spect=self;
		h=pylab.plot(spect['x'],spect['y'],linecfgstr,linewidth=linecfg['linewidth']);
		
		pfig.add_plotable(spect,linename);
		
		if showlabels:
			spect.labels();
		return h;
		
	def labels(self):
		#print "plotlabel"
		xunitobj=self.get('xunit');
		xlabel=xunitobj.getcurrentvar()+' ('+xunitobj.getcurrentunit()+')';
		xlabel=self.fixlabel(xlabel);
		pylab.xlabel(xlabel);
		yunitobj=self.get('yunit');
		ylabel=yunitobj.getcurrentvar()+' ('+yunitobj.getcurrentunit()+')';
		ylabel=self.fixlabel(ylabel);
		pylab.ylabel(ylabel);
			
		titlestr=self.get('title');
		if titlestr is not None:
			titlestr=self.fixlabel(titlestr);
			pylab.title(titlestr);

			
	def fixlabel(self,labstr):
		#print "before fix",labstr
		#labstr=labstr.replace("$","");
		#labstr=labstr.replace("\n","\rm{\n}");  # for charles
		#labstr="$"+labstr+"$";
		print labstr
		return labstr;

	#def show(self):
	#	pylab.show();
		
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
		
		menu.add_command(label="Plotxy",command=lambda:self.plot(pstyle));
		return menu;
