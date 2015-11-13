from controlframe import *;
from xyplotstyle import *;

from Tkinter import *;

class XyPlotControlFrame(ControlFrame):
	def __init__(self,master=None):
		ControlFrame.__dict__['__init__'](self, master)
		self['master']=master;
		
		pstyle=XyPlotStyle();
		self['linecolorlist']=pstyle['linecolorlist']
		self['linestylelist']=pstyle['linestylelist'];
		self['markerstylelist']=pstyle['markerstylelist'];
		
		self['optlinecolor']=StringVar();
		self['optlinestyle']=StringVar();
		self['spinlinewidth']=StringVar();
		self['spinlinewidth'].set('2');
		
		self['optmarkerstyle']=StringVar();
		self['spinmarkersize']=StringVar();
		self['spinmarkersize'].set('5');
		
		self['chkxunit'] = IntVar();
		self['chkxunit'].set(0);
		self['strxunit']=StringVar();
		self['strxunit'].set('');
		#self['chkhold'] = IntVar();
		#self['chknewfig'] = IntVar();
		#self['chkgrid'] = IntVar();
		self.__ginit();
		
	def __ginit(self):
		#frames for line and marker
		self['lineframe'] = LabelFrame(self,text='Line property');
		self['lineframe'].pack(padx=0, pady=0,fill=BOTH);
		self['markerframe'] = LabelFrame(self,text='Marker property');
		self['markerframe'].pack(padx=0, pady=0,fill=BOTH)
		
		b=self.addbutton(text="|<",command=self.resetplotstyle);
		b.pack();
		self.bindballoon(b,"Reset plotstyle");
		b=self.addbutton(text="<",command=lambda:self.nexplotstyle(-1));
		b.pack();
		self.bindballoon(b,"Previous plotstyle");
		b=self.addbutton(text=">",command=self.nexplotstyle);
		b.pack();
		self.bindballoon(b,"Next plotstyle");
		
		
		#line properties
		optlinecolor = apply(OptionMenu,(self['lineframe'],self['optlinecolor']) + tuple(self['linecolorlist']));
		self['optlinecolor'].set(self['linecolorlist'][0]);
		optlinestyle = apply(OptionMenu,(self['lineframe'],self['optlinestyle']) + tuple(self['linestylelist']));
		self['optlinestyle'].set(self['linestylelist'][0]);
		spinlinewidth=Spinbox(self['lineframe'], from_=0, to=10,width=10,textvariable=self['spinlinewidth']);
		#print self['spinlinewidth'].get()
		
		lablinecolor=Label(self['lineframe'],text='Color');
		lablinestyle=Label(self['lineframe'],text='Style');
		lablinewidth=Label(self['lineframe'],text='Width');
		
		lablinecolor.grid(row=0,column=0,sticky=W);
		lablinestyle.grid(row=1,column=0,sticky=W);
		lablinewidth.grid(row=2,column=0,sticky=W);
		optlinecolor.grid(row=0,column=1,sticky=W);
		optlinestyle.grid(row=1,column=1,sticky=W);
		spinlinewidth.grid(row=2,column=1,sticky=W);
		
		
		#marker properties
		optmarkerstyle = apply(OptionMenu,(self['markerframe'],self['optmarkerstyle']) + tuple(self['markerstylelist']));
		self['optmarkerstyle'].set(self['markerstylelist'][0]);
		spinmarkersize=Spinbox(self['markerframe'], from_=0, to=10,width=10,textvariable=self['spinmarkersize']);
		#print self['spinmarkersize'].get()
		#spinmarkersize.selection_element('2');
		
		labmarkerstyle=Label(self['markerframe'],text='Style');
		labmarkersize=Label(self['markerframe'],text='Size');
		
		labmarkerstyle.grid(row=0,column=0,sticky=W);
		labmarkersize.grid(row=1,column=0,sticky=W);
		optmarkerstyle.grid(row=0,column=1,sticky=W);
		spinmarkersize.grid(row=1,column=1,sticky=W);
		
		chkxunit = Checkbutton(self, text="Set xunit ?", variable=self['chkxunit']);
		exunit = Entry(self,textvariable=self['strxunit'],width=10);
		chkxunit.pack(side=LEFT);
		exunit.pack(side=RIGHT);
		
	def getlinecolorstr(self):
		return self['optlinecolor'].get();
	def	getlinestylestr(self):
		return self['optlinestyle'].get();
	def getlinewidth(self):
		return int(self['spinlinewidth'].get());
	def	getmarkerstylestr(self):
		return self['optmarkerstyle'].get();
	def	getmarkersize(self):
		return int(self['spinmarkersize'].get());

	def setlinecolorstr(self,linecolorstr):
		self['optlinecolor'].set(linecolorstr);
	def	setlinestylestr(self,linestylestr):
		self['optlinestyle'].set(linestylestr);
	def setlinewidth(self,linewidth):
		self['spinlinewidth'].set(str(linewidth));
	def	setmarkerstylestr(self,markerstylestr):
		self['optmarkerstyle'].set(markerstylestr);
	def	setmarkersize(self,markersize):
		self['spinmarkersize'].set(str(markersize));

	def getlineconfigstr(self):
		#print self.getlinecolorstr()
		#print self.getlinestylestr()
		#print self.getmarkerstylestr()
		return self.getlinecolorstr()+self.getlinestylestr()+self.getmarkerstylestr();
	
	def getxunit(self):
		xunit=None;
		if self['chkxunit'].get()==1:
			xunit=self['strxunit'].get();
		return xunit;
		
	def getcfg(self):
		#cfg={};
		cfg=XyPlotStyle();
		cfg['linestyle']=self.getlinestylestr();
		cfg['linecolor']=self.getlinecolorstr();
		cfg['markerstyle']=self.getmarkerstylestr();
		cfg['linewidth']=self.getlinewidth();
		cfg['markersize']=self.getmarkersize();
		cfg['xunit']=self.getxunit();
		#print "plotstylestr:",cfg.getplotstyle();
		return cfg;
		
	def setcfg(self,cfg):
		self.setlinestylestr(cfg['linestyle']);
		self.setlinecolorstr(cfg['linecolor']);
		self.setmarkerstylestr(cfg['markerstyle']);
		self.setlinewidth(cfg['linewidth']);
		self.setmarkersize(cfg['markersize']);
		
	def nexplotstyle(self,n=1):
		cfg=self.getcfg();
		cfg.nextplotstyle(n);
		self.setcfg(cfg);
		
	def resetplotstyle(self):
		cfg=XyPlotStyle();
		self.setcfg(cfg);
		