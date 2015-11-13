from dataobject import *;

class XyPlotStyle(DataObject):
	def __init__(self,pstylestr=""):
		self['linecolorlist']=["b","r", "g", "k","c","m","y"];
		self['linestylelist']=['-','--','-.',':'];
		self['markerstylelist']=['','.',',','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p','|','-'];
		
		self['linewidth']=2;
		self['markersize']=2;
		self['round']=False;
		self['linename']=None;
		self['showlabels']=True;
		self.str2obj(pstylestr);
		
	def str2obj(self,pstylestr):
		if pstylestr is None:
			pstylestr="";
		self['linecolor']=self['linecolorlist'][0];
		self['linestyle']=self['linestylelist'][0];
		self['markerstyle']=self['markerstylelist'][0];
		for k in self['linecolorlist']:
			if pstylestr.find(k)!=-1:
				pstylestr=pstylestr.replace(k,'');
				self['linecolor']=k;
		for k in self['linestylelist']:
			if pstylestr.find(k)!=-1:
				pstylestr=pstylestr.replace(k,'');
				self['linestyle']=k;
		for k in self['markerstylelist']:
			if pstylestr.find(k)!=-1:
				pstylestr=pstylestr.replace(k,'');
				self['markerstyle']=k;
				
	
	def nextlinecolor(self,n=1):
		L=len(self['linecolorlist']);
		i=self['linecolorlist'].index(self['linecolor']);
		i=i+n;
		if i>=L:
			i=i-L;
			self['round']=True;
		elif i<0:
			i=i+L;
			self['round']=True;
		self['linecolor']=self['linecolorlist'][i];
	def nextlinestyle(self,n=1):
		L=len(self['linestylelist']);
		i=self['linestylelist'].index(self['linestyle']);
		i=i+n;
		if i>=L:
			i=i-L;
			self['round']=True;
		elif i<0:
			i=i+L;
			self['round']=True;
		self['linestyle']=self['linestylelist'][i];
	def nextmarkerstyle(self,n=1):
		L=len(self['markerstylelist']);
		i=self['markerstylelist'].index(self['markerstyle']);
		i=i+n;
		if i>=L:
			i=i-L;
			self['round']=True;
		elif i<0:
			i=i+L;
			self['round']=True;
		self['markerstyle']=self['markerstylelist'][i];
		
	def getplotstyle(self):
		return self['markerstyle']+self['linestyle']+self['linecolor'];
		
	def nextplotstyle(self,n=1):
		self['round']=False;
		self.nextlinecolor(n);
		if self['round'] is True:
			self['round']=False;
			self.nextlinestyle(n);
		if self['round'] is True:
			self['round']=False;
			self.nextmarkerstyle(n);
			