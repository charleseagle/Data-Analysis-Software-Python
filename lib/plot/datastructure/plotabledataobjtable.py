from dataobjtable import *;
from xpyfigure import *;
from xyplotstyle import *;
from xyplotable import *;
from xyzplotable import *;
from plotcontrol import *;
import easygui;
import numpy;

class PlotableDataObjTable(DataObjTable,PlotControl):
	def __init__(self):
		DataObjTable.__dict__['__init__'](self);

	def plot(self,pstyle="-"):
		import pylab;
		pfig=XpyFigure(pylab.gcf().number);

		if isstring(pstyle):
			pstyle=XyPlotStyle(pstyle);
		i=0;
		pylab.ioff();
		#print "ioff"
		for k in self.keys():
			p=self[k];
			if self.get('_datobj_title') is not None:
				p['title']=self.get('_datobj_title');
				#print "p type",type(p)
			pstyle['linename']=k;
			if i==0:
				pstyle['showlabels']=True;
			else:
				pstyle['showlabels']=False;
			p.plot(pstyle);
			if i==0:
				pylab.hold(True);
			pstyle.nextplotstyle();
				
			i=i+1;	
		pylab.ion();
		pylab.grid(True);
		stdout( "plotabledataobjtable:plot, done.")

		
	def contextmenu(self,menu,dataname=None):
		import os,time;
		menu=DataObjTable.contextmenu(self,menu);
		menu.add_separator();
		menu=PlotControl.contextmenu(self,menu);
		topwin=gettoplevelmaster(menu);
		pstyle=XyPlotStyle();
		#pstyle['title']=os.path.join(topwin['savepath'],topwin['winname'])+'['+time.ctime()+']';
		#menu=XyDiscreteFun.__dict__['contextmenu'](self,menu);
		savepath=topwin['savepath'];
		if savepath is None:
			savepath='';
		self['_datobj_title']=os.path.join(savepath,topwin['winname'])+'['+time.ctime()+']';
		self['_datobj_title']=self['_datobj_title'].replace("\\",":")
		self['_datobj_title']=self['_datobj_title'].replace("_",".")
		menu.add_command(label="Xyplot",command=lambda:self.plot(pstyle));
		menu.add_command(label="Convert 2 XyPlotable",command=self.uicolumn2xy);
		menu.add_command(label="Image",command=lambda: self.uiconvert2xyz(plot2dtype="image"));
		menu.add_command(label="Contour",command=lambda: self.uiconvert2xyz(plot2dtype="contour"));
		return menu;
		
	def uicolumn2xy(self,xcolumn=None,ycolumn=None):
		spect=None;
		rownames=self.keys();
		#print "1st rowname",rownames[0]
		numcolumns=self[rownames[0]].numerickeys();
		if xcolumn is None:
			answer=easygui.choicebox("Pick x column","Convert columns to XyPlotable",numcolumns);
			xcolumn=answer;
		if xcolumn is not None:
			#print "xcolumn"
			if ycolumn is None:
				answer=easygui.choicebox("Pick y column","Convert columns to XyPlotable",numcolumns);
				ycolumn=answer;
			if ycolumn is not None:
				spect=self.column2xy(xcolumn,ycolumn);
				spect.plot()
		return spect;
	
	def column2xy(self,xcolumn,ycolumn):
		#print xcolumn,ycolumn
		xlist=self.aggselect(xcolumn);
		ylist=self.aggselect(ycolumn);
		spect=XyPlotable();
		spect['x']=numpy.array(xlist);
		spect['y']=numpy.array(ylist);
		spect['xunit'].setcurrentunit(varname=xcolumn);
		spect['yunit'].setcurrentunit(varname=ycolumn);
		spect.sortx();
		return spect;
	
	def uiconvert2xyz(self,newycolumn=None,plot2dtype="image",linecfg=None):
		spect=None;
		rownames=self.keys();
		#print "1st rowname",rownames[0]
		numcolumns=self[rownames[0]].numerickeys();
		if newycolumn is None:
			answer=easygui.choicebox("Pick y column","Convert columns to XyzPlotable",numcolumns);
			newycolumn=answer;
		if newycolumn is not None:
			spect=self.convert2xyz(newycolumn);
			if plot2dtype=="image":
				spect.image(linecfg=linecfg);
			elif plot2dtype=="contour":
				spect.contour(linecfg=linecfg);
		return spect;

	def convert2xyz(self,newycolumn):
		ylist=self.aggselect(newycolumn);
		spect=XyzPlotable();
		keys=self.keys();
		z=self[keys[0]]['y'];
		x=self[keys[0]]['x'];
		for i in range(1,len(keys)):
			k=keys[i];
			z=numpy.vstack((z,self[k]['y']));
		spect['x']=x;
		spect['y']=numpy.array(ylist);
		spect['z']=z;
		spect['xunit']=self[keys[0]]['xunit'];
		spect['yunit'].setcurrentunit(unitname=newycolumn);
		spect.interp();
		return spect;

	def uipickcolumnvalue(self,x0,newycolumn=None):
		spect=None;
		rownames=self.keys();
		#print "1st rowname",rownames[0]
		numcolumns=self[rownames[0]].numerickeys();
		if newycolumn is None:
			answer=easygui.choicebox("Pick new x column","pick column",numcolumns);
			newycolumn=answer;
		if newycolumn is not None:
			spect=self.pickcolumnvalue(x0,newycolumn);
		return spect;
		
	def pickcolumnvalue(self,x0,newycolumn):
		ylist=self.aggselect(newycolumn);
		spect=XyPlotable();
		keys=self.keys();
		
		x=numpy.array(ylist);
		y=x-x+0.0;
		print 'x0',x0
		for i in range(len(keys)):
			k=keys[i];
			x[i]=self[k][newycolumn];
			y[i]=self[k](x0);
			#print x[i],y[i],self[k](x0)
		spect['x']=x;
		spect['y']=y;
		return spect;