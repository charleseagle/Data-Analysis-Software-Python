from dataobject import *;
from units import *;
from xpyfun import *;
from xos import *;
import pylab;
import scipy.interpolate;
import scipy.optimize;
import scipy;
import numpy;
import copy;
import os;

class XyDiscreteFun(DataObject):
	def __init__(self):
		self['xunit']=Units();
		self['yunit']=Units();

	def __call__(self,x):
		if issubclass(type(x),list): 
			y=scipy.interp(x,self['x'],self['y']);
		else:
			y=scipy.interp([x],self['x'],self['y']);
			y=y[0];
		return y;
		
	def shift(self,delta):
		self['x']=self['x']+delta;
		
	def exportascii(self,farg,dataname=''):
		DataObject.exportascii(self,farg,dataname);
		x=XOS();
		if isinstance(farg,str):
			fname=farg;
		else:
			fh=farg;
			fname=fh.name;
		myfname=x.filenameappend(fname,dataname+'_xy');
		print "Exporting "+dataname+"[XyDiscreteFun] to:",myfname
		myfh=open(myfname,'w');
			
		for i in range(len(self['x'])):
			myfh.write(str( self['x'][i])+','+str(self['y'][i]));
			myfh.write("\n");
		myfh.close();
		
	def numstrsetting(self):
		self.uiset(datatype='string');
		self.uiset(datatype='numeric');
		
	def copynumstrsettingto(self,anotherfun):
		for k in self.keys():
			if isstring(self[k]) or isnumeric(self[k]):
				anotherfun[k]=self[k];
				

#=========================================================================
# mono spect operation
#=========================================================================
	def update(self,_updatecmd):
		_oldkeys=self.keys();
		for _iupdaterow in self.keys():
			_cmd=_iupdaterow+"=self['"+_iupdaterow+"']";
			exec(_cmd);
		exec(_updatecmd);
		#print "updatecmd:",_updatecmd
		#print "Temperature:",Temperature
		for _iupdaterow in _oldkeys:
			_cmd="self['"+_iupdaterow+"']="+_iupdaterow;
			exec(_cmd);

	def cumsum(self,xmin=None,xmax=None):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		
		#xomega=2*numpy.pi*3e8*x*1e2;
		#neff0=self['y'][0]*xomega[0];
		sum0=y[0];
		sum=x-x;
		for i in range(len(x)):
			if i==0:
				sum[i]=sum0;
			else:
				sum[i]=sum[i-1]+y[i]*(x[i]-x[i-1]);
		spect['y']=sum;
		return spect;
	
	def integral(self,xmin=None,xmax=None):
		cumsumspect=self.cumsum(xmin,xmax);
		result=cumsumspect['y'][-1];
		return result;
	
	def wheremax(self,xmin=None,xmax=None):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		I=argmax(y);
		x_max=x[I];
		return x_max;
		
	def wheremin(self,xmin=None,xmax=None):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		I=argmin(y);
		x_min=x[I];
		return x_min;	
		
	def copyxy(self):
		sp=self.copy();
		sp['num_matrix']=None;
		return sp;
		
	def convertx(self,tounit):
		xunit=self['xunit'];
		#print "xunit:",xunit
		x=self['x'];
		x=xunit.convert(x,tounit);
		self['x']=x;
		self.sortx();
		
	def sortx(self):
		I=numpy.argsort(self['x']);
		self['x']=self['x'][I];
		self['y']=self['y'][I];
	
	
	def pick(self,xmin=None,xmax=None,ymin=None,ymax=None,nonempty=None):
		#self.sortx();
		eps=self['xunit'].getcurrenttolerance();
		#print "eps",eps
		x=self['x'].copy();
		y=self['y'].copy();
		Imin=-len(x);
		Imax=len(x);
		if xmin is None:
			xmin=min(x);
		if xmax is  None:
			xmax=max(x);
		if ymin is  None:
			ymin=min(y);
		if ymax is  None:
			ymax=max(y);
		
		x1=self['x'][(x-xmin)<=eps];
		if len(x1)>0:
			Imin=len(x1);
		x2=self['x'][(x-xmax)>=-eps];
		if len(x2)>0:
			Imax=len(x)-len(x2)-1;
			
		I=numpy.core.logical_and((x-xmin)>=-eps, (x-xmax)<=eps);
		#x=x[I];
		#y=y[I];	
			
		#if len(x)>0:
		I=numpy.core.logical_and(I,y>=ymin);
		I=numpy.core.logical_and(I,y<=ymax);
		
		x=x[I];
		y=y[I];
			
		if nonempty is not None and len(x)<nonempty:
			dx=xmax-xmin;
			dy=ymax-ymin;
			xmin1=xmin-dx/2;
			xmax1=xmax+dx/2;
			ymin1=ymin-dy/2;
			ymax1=ymax+dy/2;
			Imin,Imax=self.pick(xmin1,xmax1,ymin1,ymax1,1);
		else:
			self['x']=x;
			self['y']=y;
		
		#print "lenx",len(x)
		#print "nonempty:",nonempty
		return (Imin,Imax);
		
	def yconstrain(self,ymin=None,ymax=None):
		try:
			eps=self['yunit'].getcurrenttolerance();
		except:
			eps=1e-9;
		y=self['y'];
		if ymin is None:
			ymin=min(y);
		if ymax is None:
			ymax=max(y);
		Iin=numpy.core.logical_and((y-ymin)>=-eps, (y-ymax)<=eps);
		Ilow=(y-ymin)<-eps;
		Ihigh=(y-ymax)>eps;
		ylow=min(y[Iin]);
		yhigh=max(y[Iin]);
		y[Ilow]=ylow+numpy.zeros(len(y[Ilow]));
		y[Ihigh]=yhigh+numpy.zeros(len(y[Ihigh]));
		
	def refine(self,resolution):
		xmin=self['x'].min();
		xmax=self['x'].max();
		xrefine=arange(xmin,xmax,resolution);
		yrefine=self(xrefine);
		#spect=copy.deepcopy(self);
		self['x']=xrefine;
		self['y']=yrefine;
		#return spect;
		
	def cull(self,resolution,xmin=None,xmax=None):
		self.sortx();
		x=self['x'];
		if xmin is None:
			xmin=min(x);
		if xmax is None:
			xmax=max(x);
		spect=self.copyxy();
		Imin,Imax=spect.pick(xmin,xmax);
		evenoddsign=1;
		while spect.summarize()['res_min']<resolution:
			#print "before",spect.summarize()['res_min']
			spect.cullonce(resolution,(evenoddsign+1)/2);
			evenoddsign=evenoddsign*-1;
			#print "culled once."
			#print "after",spect.summarize()['res_min']
		self['x']=numpy.hstack((spect['x'][0:Imin-1],spect['x'],spect['x'][Imax+1:]));
		self['y']=numpy.hstack((spect['y'][0:Imin-1],spect['y'],spect['y'][Imax+1:]));
		
		
	def cullonce(self,resolution,evenoddchoice):
		x=self['x'];
		difx=numpy.diff(x);
		difx=numpy.hstack((difx,resolution*2));
		I1=range(len(x));

		I=numpy.core.logical_or(difx>resolution, pylab.mod(I1,2)==evenoddchoice);
		#I=[];
		#i=0;
		#while i <len(difx):
		#	I.append(i);
		#	if difx[i]<resolution:
		#		i=i+2;
		#	else:
		#		i=i+1;
		#I.append(len(x)-1);
		#I=numpy.array(I);
		#print "shape before",x.shape
		self['x']=self['x'][I];
		self['y']=self['y'][I];
		#print "shape after",self['x'].shape
	
	def smooth(self,xwidth=None,xmin=None,xmax=None,xwidthN=100,base=1,edgeconserve=1):
		if xmin is None:
			xmin=min(self['x']);
		if xmax is None:
			xmax=max(self['x']);
		if xwidth is None:
			xwidth=(xmax-xmin)/xwidthN;
		spect=self.copyxy();
		spect.pick(xmin,xmax,nonempty=3);
		#print "widthratio:",xwidth/(xmax-xmin)
		spect.gaussconv(xwidth,base=base,edgeconserve=edgeconserve);
		if len(spect['x'])<len(self['x']):
			spect.extend(self,smooth=0);
		self['x']=spect['x'];
		self['y']=spect['y'];
		
	def gaussconv(self,xwidth,base=0,edgeconserve=0):
		x=self['x'];
		y=self['y'];
		if len(x)>=2:
			dx1=min(numpy.fabs(numpy.diff(x)));
			dx2=numpy.mean(numpy.fabs(numpy.diff(x)))/10;
			dx=max(dx1,dx2);
			N=int(numpy.ceil((max(x)-min(x))/dx));
			dx=(max(x)-min(x))/N;
		
			#xint=xarange(min(x),max(x)+dx,dx);
			xint=scipy.linspace(min(x),max(x),N+1);
			self_b=self.copyxy();
			self_b.addshoulder();
			int1=scipy.interpolate.interp1d(self_b['x'],self_b['y']);
			yint=int1(xint);
		
			spectint=self.copyxy();
			spectint['x']=xint;
			spectint['y']=yint;
			spectint.addshoulder();
			xint=spectint['x'];
			yint=spectint['y'];

			Ng=int(numpy.ceil(3*xwidth/dx));
		#print "Ng:",Ng
		#print "dx",dx;
		#print "xwidth",xwidth
		#xg=numpy.arange(-Ng*dx,Ng*dx+dx,dx);
		#if len(xg)%2==0:
		#	xg=numpy.hstack((xg,Ng*dx+dx));
		#xg=xarange(-Ng*dx,Ng*dx+dx,dx);
			xg=scipy.linspace(-Ng*dx,Ng*dx,Ng*2+1);
			yg=numpy.exp(-numpy.power(xg/xwidth,2)/2);
		#print "lyg",len(yg);
		
			if base==1:
				P=numpy.polyfit(numpy.array([xint[0],xint[-1]]),numpy.array([yint[0],yint[-1]]),1);
			#print "lx",len(xint),"ly",len(yint)
				ybase=numpy.polyval(P,xint);
			#print "len:",len(ybase)
				yint=yint-ybase;
			#pylab.plot(x,y);
			#pylab.hold(True);
			#pylab.plot(x,ybase);

			yconv=numpy.convolve(yint,yg)/yg.sum();
			yconv=yconv[Ng:-Ng];
		#print "Ly:",len(y),"Lyconv",len(yconv)
		#pylab.plot(x,yconv);
			if base==1:
				yconv=yconv+ybase;
		#print "Lx:",len(x),"Ly",len(y);	
			int2=scipy.interpolate.interp1d(xint,yconv);
			ynew=int2(x);
		#pylab.plot(self['x'],ynew);
		
			if edgeconserve==1:
			#P=numpy.polyfit(numpy.array([x[0],x[-1]]),numpy.array([y[0],y[-1]]),1);
			#ybase=numpy.polyval(P,x);
				ybase=self.getbaseline();
				spect0=self.copyxy();
				spect0['y']=spect0['y']-ybase;
				M0=spect0.nthmoment(0);
			
				spect0['y']=ynew;
				ybase0=spect0.getbaseline();
				spect0['y']=spect0['y']-ybase0;
				M1=spect0.nthmoment(0);
			#print "M1:",M1,"M0:",M0
				if M1!=0:
					spect0['y']=spect0['y']*M0/M1;
				self['y']=spect0['y']+ybase;
			else:
				self['y']=ynew;
		
		
	def inverse(self):
		spect['y']=1/spect['y'];
		
	def fixglich(self,xmin,xmax):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		P=numpy.polyfit(numpy.array([min(x), max(x)]), numpy.array([y[0], y[-1]]),1);
		ypoly=numpy.polyval(P,x);
		spect['y']=ypoly;
		spect.extend(self,smooth=1);
		self['y']=spect['y'];

	def yerrmean(self):
		y=self['y'];
		yerr=self['yerr'];
		yerr=nonzeroarray(yerr,1e-9);
		return (y/yerr).sum()/(1/yerr).sum();
		
	def addshoulder(self,xmin=None,xmax=None):
		self.sortx();
		x=self['x'];
		y=self['y'];
		#dx=None;
		if xmin is None:
			#dx=numpy.mean(numpy.fabs(numpy.diff(x)));
			dx=x[1]-x[0];
			xmin=min(x)-dx;
		if xmax is None:
			#if dx is None:
			#	dx=numpy.mean(numpy.fabs(numpy.diff(x)));
			dx=x[-1]-x[-2];
			xmax=max(x)+dx;
		xint=numpy.hstack((xmin,x,xmax));
		yint=numpy.hstack((y[0],y,y[-1]));
		self['x']=xint;
		self['y']=yint;
		

	def uniquex(self,error=1e-9):
		x=self['x'];
		I=numpy.fabs(numpy.diff(x))>=error;
		#print min(numpy.fabs(numpy.diff(x)));
		#print "len I",len(I)
		while len(x[I])<len(x)-1:
			self['x']=self['x'][I];
			self['y']=self['y'][I];
			x=self['x'];
			I=numpy.fabs(numpy.diff(x))>=error;
			
	def nthmoment(self,n):
		x=self['x'];
		y=self['y']
		dx=numpy.fabs(numpy.diff(x));
		dx=numpy.hstack((dx,dx[-1]));
		xmean=(x*y*dx).sum()/(y*dx).sum();
		if n==0:
			moment=(y*dx).sum();
		elif n==1:
			moment=xmean;
		else:
			moment=(numpy.power(x-xmean,n)*y*dx).sum()/(y*dx).sum();
		return moment;
	
	def getbaseline(self):
		x=self['x'];
		y=self['y'];
		P=numpy.polyfit(numpy.array([x[0],x[-1]]),numpy.array([y[0],y[-1]]),1);
		#print "lx",len(xint),"ly",len(yint)
		ybase=numpy.polyval(P,x);
		return ybase;
	
	def smoothstep(self,xmin,xmax):
		x=self['x'];
		spect=self.copyxy();
		I=numpy.core.logical_and(x>=xmin, x<=xmax);
		spect['x']=spect['x'][I];
		spect['y']=spect['y'][I];
		y0=spect['y'][0];
		yend=spect['y'][-1];
		smoothwidth=(max(spect['x'])-min(spect['x']))/4;
		for i in range(5):
			spect.gaussconv(smoothwidth,base=1);
			spect['y'][0]=y0;
			spect['y'][-1]=yend;
		self['y'][I]=spect['y'];
	
	def polyfit(self,n,xmin=None,xmax=None):
		if xmin is None:
			xmin=min(self['x']);
		if xmax is None:
			xmax=max(self['y']);
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		P=numpy.polyfit(spect['x'],spect['y'],n);
		yfit=numpy.polyval(P,spect['x']);
		check=numpy.core.maximum(numpy.core.fabs(yfit),numpy.core.fabs(spect['y']));
		dy=sqrt(((yfit-spect['y'])**2/check).sum()/(1/check).sum());
		return (P,dy);
		
	def gaussfit(self,xmin=None,xmax=None,method=None):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		
		center=spect.nthmoment(1);
		width=spect.nthmoment(2)**0.5;
		amp=spect.nthmoment(0)*2/(max(x)-min(x));
		slope=0;
		intercept=0;
		if method=="baseslope" or method==2:
			paras0=pylab.array([amp,center,width,slope,intercept]);
			paras=scipy.optimize.fmin(self.gaussfit_baseslope_chi2,paras0,args=(x,y));
		elif method=="base" or method==1:
			paras0=pylab.array([amp,center,width,intercept]);
			paras=scipy.optimize.fmin(self.gaussfit_base_chi2,paras0,args=(x,y));
			lp=list(paras)
			lp.append(0);
			paras=numpy.array(lp);
		elif method is None or method==0:
			paras0=pylab.array([amp,center,width]);
			paras=scipy.optimize.fmin(self.gaussfit_chi2,paras0,args=(x,y));
			lp=list(paras);
			lp.append(0);lp.append(0);
			paras=numpy.array(lp);
		return paras;
	
	def expdecayfit(self,xmin=None,xmax=None):
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		x=spect['x'];
		y=spect['y'];
		
		I0=y[0]-y[-1];
		tau=spect.nthmoment(2)**0.5;
		baseline=mean(y);
		
		paras0=pylab.array([I0,tau,baseline]);
		paras=scipy.optimize.fmin(self.expdecayfit_chi2,paras0,args=(x,y));
		
		I0=paras[0];
		tau=paras[1];
		baseline=paras[2];
		
		yfit=I0*exp(-x/tau)+baseline;
		check=numpy.core.maximum(numpy.core.fabs(y),numpy.core.fabs(yfit));
		
		spect.plot();pylab.hold(True);
		pylab.plot(x,yfit,'r');pylab.hold(False);
		#pylab.show();
		
		#chi2=self.expdecayfit_chi2(paras,x,y);
		#dchi2dtau=(2*(y-yfit)/check*I0*exp(-x/tau)*x/tau**2).sum();
		#dchi2dtau=(2*(y-yfit)*I0*exp(-x/tau)*x/tau**2).sum();
		#tauerror=pylab.fabs(chi2/dchi2dtau);
		#check=1;
		chi2I0I0=(2*exp(-2*x/tau)/check).sum();
		chi2I0tau=(2*(yfit-y)*exp(-x/tau)*x/tau**2/check+2*I0*exp(-2*x/tau)*x/tau**2/check).sum();
		chi2tautau=(2*I0*exp(-2*x/tau)*x**2/tau**4/check+2*(yfit-y)*I0*exp(-x/tau)*x**2/tau**4/check-4*(yfit-y)*I0*exp(-x/tau)*x/tau**2/check).sum();
		errormatrix=pylab.array([[chi2I0I0,chi2I0tau],[chi2I0tau,chi2tautau]]);
		#print 'errormatrix',errormatrix
		inverr=scipy.linalg.inv(errormatrix);
		#print 'inverr',inverr
		tauerror=(pylab.fabs(inverr[1][1]))**0.5;
		print 'tauerror',tauerror
		
		return (paras,tauerror);
	
	def fixjump(self,xmin,xmax,norder=1,npoints=20):
		spectL=self.copyxy();
		spectL.pick(xmax=xmin);
		spectR=self.copyxy();
		spectR.pick(xmin=xmax);
		spectM=self.copyxy();
		spectM.pick(xmin=xmin,xmax=xmax);
		spL=spectL.copyxy();
		spR=spectR.copyxy();
		spL['x']=spL['x'][-npoints:];
		spL['y']=spL['y'][-npoints:];
		spR['x']=spR['x'][:npoints];
		spR['y']=spR['y'][:npoints];
		spR.nonoverlaprenormpoly(spL,norder);
		gainfactor=spR.getfromlog(-1,"gainfactor");
		#x=numpy.hstack((spectL['x'],spectR['x']));
		#y=numpy.hstack((spectL['y'],spectR['y']*gainfactor));
		P=spR['poly'];
		x=numpy.hstack((spectL['x'],spectM['x'],spectR['x']));
		y=numpy.hstack((spectL['y'],pylab.polyval(P,spectM['x']),spectR['y']*gainfactor));
		self['x']=x;
		self['y']=y;
		self.log({"method":"fixjump","gainfactor":gainfactor});
		
	def fixnotch(self,xmin,xmax,norder=1,npoints=20):
		spectL=self.copyxy();
		spectL.pick(xmax=xmin);
		spectR=self.copyxy();
		spectR.pick(xmin=xmax);
		spectM=self.copyxy();
		spectM.pick(xmin=xmin,xmax=xmax);
		spL=spectL.copyxy();
		spR=spectR.copyxy();
		spL['x']=spL['x'][-npoints:];
		spL['y']=spL['y'][-npoints:];
		spR['x']=spR['x'][:npoints];
		spR['y']=spR['y'][:npoints];
		x=numpy.hstack((spL['x'],spR['x']));
		y=numpy.hstack((spL['y'],spR['y']));
		PR=numpy.polyfit(x,y,norder);
		
		x=numpy.hstack((spectL['x'],spectM['x'],spectR['x']));
		y=numpy.hstack((spectL['y'],pylab.polyval(PR,spectM['x']),spectR['y']));
		self['x']=x;
		self['y']=y;
		self.log({"method":"fixnotch","poly":PR});
		
		
	def fft(self):
		self.sortx();
		xmin=min(self['x']);
		xmax=max(self['x']);
		dx=numpy.fabs(numpy.mean(diff(self['x'])));
		Nx=(xmax-xmin)/dx;
		xnew=numpy.linspace(xmin,xmax,Nx+1);
		spect=self.copyxy();
		spect['x']=xnew;
		spect['y']=xnew;
		spect1=self.copyxy();
		spect1.mapx(spect);
		newy=pylab.fft(spect1['y']);
		newx=arange(len(spect1['x']))/float(len(spect1['x']))/dx;
		spect1['x']=newx;
		spect1['y']=newy.real;
		return spect1;
		
#=================================================================
#=================================================================
# binary operation
#=================================================================
	def binop(self,spect2,op):
		spect=spect2.copyxy();
		spect.mapx(self);
		#print type(spect)
		#self['ybak']=copyxy.copy(self['y']);
		cmd="self['y']=self['y']"+op+"spect['y']";
		#print "cmd:",cmd;
		exec(cmd);
		
	def divideby(self,dividerspect):
		spect=dividerspect.copyxy();
		spect.mapx(self);
		#self['ybak']=copy.copy(self['y']);
		self['y']=self['y']/spect['y'];
	
	def subtract(self,spect2subtract):
		spect=spect2subtract.copyxy();
		spect.mapx(self);
		#self['ybak']=copy.copy(self['y']);
		self['y']=self['y']-spect['y'];
		
	def ratio(self,spect2):
		if self.has_key('yerr'):
			yerr=self['yerr'];
		else:
			yerr=numpy.sqrt(numpy.fabs(self['y']));
		if spect2.has_key('yerr'):
			y2err=spect2['yerr'];
		else:
			y2err=numpy.sqrt(numpy.fabs(spect2['y']));
		
		y=self['y'];
		y2=spect2['y'];
		#print "len y:",len(y),"len y2:",len(y2)
		y2nz=nonzeroarray(y2.copy(),1e-9);
		ynew=y/y2nz;
		
		ynewerr2=(y*y*y2err*y2err)/y2nz/y2nz/y2nz/y2nz+yerr*yerr/y2nz/y2nz;
		self['y']=ynew;
		self['yerr']=nonzeroarray(numpy.sqrt(ynewerr2),1e-9);
	
	def conv(self,spect2):
		sp1=self.copyxy();
		sp2=spect2.copyxy();

		center1=sp1.nthmoment(1);
		center2=sp2.nthmoment(1);
		sp1.shift(-center1);
		sp2.shift(-center2);
		
		resolution=min(mean(abs(diff(sp1['x']))),mean(abs(diff(sp2['x']))));
		x1=arange(min(sp1['x']),max(sp1['x'])+resolution,resolution);
		x2=arange(min(sp2['x']),max(sp2['x'])+resolution,resolution);
		
		yf=sp1(x1);
		yg=sp2(x2);
		yconv=numpy.convolve(yf,yg);
		yconv=yconv*resolution;
		xmin_conv=min(sp1['x'])+min(sp2['x']);
		xmax_conv=max(sp1['x'])+max(sp2['x']);
		xconv=arange(xmin_conv,xmax_conv+resolution,resolution);
		if len(xconv)>=len(yconv):
			xconv=xconv[0:len(yconv)];
		else:
			while len(xconv)<len(yconv):
				xconv=list(xconv)+[xconv[-1]+resolution];
				xconv=array(xconv);
		resultspect=self.copyxy();
		resultspect['x']=xconv+center1+center2;
		resultspect['y']=yconv;
		#print "m0:",self.nthmoment(0),spect2.nthmoment(0),resultspect.nthmoment(0),resolution
		#print "m1:",self.nthmoment(1),spect2.nthmoment(1),resultspect.nthmoment(1)
		#print "m2:",self.nthmoment(2),spect2.nthmoment(2),resultspect.nthmoment(2)
		return resultspect;
		
	def deconv(self,spect2,Nmax=100,alpha=0.1):
		# self is the convolution of spect2 and the spect to find
		#Nmax=100;
		eps=1e-3;
		lamb=1e-2;
		lamb=alpha;
		
		m0ratio=self.nthmoment(0)/spect2.nthmoment(0);
		m1diff=self.nthmoment(1)-spect2.nthmoment(1);
		m2diff=abs(self.nthmoment(2)-spect2.nthmoment(2));
		#print "m0ratio",self.nthmoment(0),spect2.nthmoment(0)
		#print "m1diff",self.nthmoment(1),spect2.nthmoment(1)
		#print "m2diff",self.nthmoment(2),spect2.nthmoment(2)
		
		xgauss=self['x']-self.nthmoment(1)+m1diff;
		ygauss=exp(-(xgauss-m1diff)**2/2/m2diff);
		ygauss=ygauss/ygauss.sum()*m0ratio;
		spectgauss=self.copyxy();
		spectgauss['x']=xgauss;
		spectgauss['y']=ygauss;
		
		
		chi=1e10;
		spectresult=spectgauss;
		spectdiff=self.copyxy();
		spectdiff['y']=self['x']-self['x'];
		
		n=0;
		while n<Nmax and chi>eps:
			spectresult['y']=spectresult['y']-spectdiff['y']*lamb;
			spectresult['y']=abs(spectresult['y']);
			spectconv=spect2.conv(spectresult);
			yconv=spectconv(self['x']);
			spectconv['x']=self['x'];
			spectconv['y']=yconv;
			spectdiff=spectconv.copyxy();
			spectdiff['y']=yconv-self['y'];
			chi=spectdiff['y']**2/(abs(self['y'])+abs(yconv));
			chi=chi.mean();
			n=n+1;
			print "n,chi:",n,chi
		if n>=Nmax:
			print "reached Nmax for deconv"
		else:
			print "reached eps for deconv"
		return spectresult;
		
	def diff(self,spect2):
		if self.has_key('yerr'):
			yerr=self['yerr'];
		else:
			yerr=numpy.sqrt(numpy.fabs(self['y']));
		if spect2.has_key('yerr'):
			y2err=spect2['yerr'];
		else:
			y2err=numpy.sqrt(numpy.fabs(spect2['y']));
		y=self['y'];
		y2=spect2['y'];
		ynew=y-y2;
		ynewerr2=numpy.sqrt(yerr*yerr+y2err*y2err);
		self['y']=ynew;
		self['yerr']=nonzeroarray(numpy.sqrt(ynewerr2),1e-9);
		
	def renorm(self,xyfunstandard,xmin=None,xmax=None,gainorshift=0):
		xmincom,xmaxcom=self.commonrange(xyfunstandard);
		if xmin is None:
			xmin=xmincom;
		if xmax is None:
			xmax=xmaxcom;
			
		x,y1,y2=self.getcommonxy(xyfunstandard,xmin,xmax);
		if gainorshift==0: # gain
			paras=scipy.optimize.leastsq(self.renormgain_chi2,1,args=(y1,y2));
		#print "optparas",paras[0]
			self['y']=self['y']*paras[0];
		elif gainorshift==1: #shift
			paras=scipy.optimize.leastsq(self.renormshift_chi2,0,args=(y1,y2));
			self['y']=self['y']+paras[0];
		elif gainorshift==2:
			paras0=(1., 0.);
			paras=scipy.optimize.fmin(self.renormboth_chi2,paras0,args=(y1,y2));
			print paras
			#self['y']=self['y']+(self['x']-min(self['x']))*paras[0]+paras[1];
			self['y']=self['y']*paras[0]+paras[1];
		elif gainorshift==3:
			paras0=(1., 0.);
			paras=scipy.optimize.fmin(self.renormramp_chi2,paras0,args=(x,y1,y2));
			#print paras
			#self['y']=self['y']+(self['x']-min(self['x']))*paras[0]+paras[1];
			self['y']=self['y']*(paras[0]+paras[1]*self['x']);	
		elif gainorshift==4:
			paras0=(1., 0.,0.);
			paras=scipy.optimize.fmin(self.renormrampshift_chi2,paras0,args=(x,y1,y2));
			#print paras
			#self['y']=self['y']+(self['x']-min(self['x']))*paras[0]+paras[1];
			self['y']=self['y']*(paras[0]+paras[1]*self['x'])+paras[2];
	
	def nonoverlaprenormpoly(self,spect,norder=1):
		PR=numpy.polyfit(self['x'],self['y'],norder);
		PL=numpy.polyfit(spect['x'],spect['y'],norder);
		#x=numpy.hstack(self['x'],spect['x']);
		xR=self['x'];
		xL=spect['x'];
		yR=self['y'];
		yL=spect['y'];
		gainfactor=1;
		P=(PL+PR)/2;
		paras0=numpy.hstack((gainfactor,P));
		paras=scipy.optimize.fmin(self.noneoverlap_renormgain_chi2,paras0,args=(xL,yL,xR,yR));
		gainfactor=paras[0];
		self['y']=self['y']*gainfactor;
		self['poly']=paras[1:];
		self.log({"method":"nonoverlaprenormpoly","gainfactor":gainfactor});
		
		
	def meanmerge(self,spect,xmin=None,xmax=None):
		x,y1,y2=self.getcommonxy(spect,xmin,xmax);
		#print "Lx:",len(x)
		if x is None:
			newx=numpy.hstack((self['x'],spect['x']));
			newy=numpy.hstack((self['y'],spect['y']));
		else:
			if xmin is None:
				xmin=min(x);
			if xmax is None:
				xmax=max(x);
			xsigma=(xmax-xmin)/4;
			IL=x<xmin;
			xL=x[IL];
			yL=y1[IL];
			IR=x>xmax;
			xR=x[IR];
			yR=y2[IR];
			IMid=numpy.core.logical_and(x>=xmin, x<=xmax);
			xMid=x[IMid];
			yMid=(y1[IMid]*numpy.exp(-numpy.power((xMid-xmin)/xsigma,2)/2)+y2[IMid]*numpy.exp(-numpy.power((xMid-xmax)/xsigma,2)/2))/(numpy.exp(-numpy.power((xMid-xmin)/xsigma,2)/2)+numpy.exp(-numpy.power((xMid-xmax)/xsigma,2)/2));
		#print "midlen:",len(xMid),len(yMid)
		#print "Llen:",len(xL),len(yL);
		#print "Rlen:",len(xR),len(yR);
		
			ycommon=numpy.hstack((yL,yMid,yR));
		#print "xlen:",len(x),len(ycommon)
		
			IL=self['x']<min(x);
			xL=self['x'][IL];
			yL=self['y'][IL];
			IR=spect['x']>max(x);
			xR=spect['x'][IR];
			yR=spect['y'][IR];
			newx=numpy.hstack((xL,x,xR));
			newy=numpy.hstack((yL,ycommon,yR));
		#print "lx",len(newx),"ly",len(newy)
		self['x']=newx;
		self['y']=newy;
		self.uniquex();
		
	def indmerge(self,spect1,xmin,xmax,gainorshift=0):
		x,y1,y2=self.getcommonxy(spect1,xmin,xmax);
		if self.renormshift_chi2(0,y1,y2)>1e-9:
			if gainorshift==0:
				paras=scipy.optimize.leastsq(self.renormgain_chi2,1,args=(y2,y1));
				spect1['y']=spect1['y']*paras[0];
			elif gainorshift==1:
				paras=scipy.optimize.leastsq(self.renormshift_chi2,1,args=(y2,y1));
				spect1['y']=spect1['y']+paras[0];
			elif gainorshift==2:
				paras=[1];
		#print "optparas",paras[0]
		
			self.meanmerge(spect1,xmin,xmax);
			self.log({"gainfactor":paras[0],"xmin":xmin,"xmax":xmax});
			return paras[0];
		else:
			self.meanmerge(spect1,xmin,xmax);
			if gainorshift==0:
				return	1;
			elif gainorshift==1:
				return 0;
		
	def extend(self,broaderspect,smooth=0):
		b=broaderspect;
		xmin,xmax=self.commonrange(b);
		IL=b['x']<xmin;
		IR=b['x']>xmax;
		newx=numpy.hstack((b['x'][IL],self['x'],b['x'][IR]));
		newy=numpy.hstack((b['y'][IL],self['y'],b['y'][IR]));
		self['x']=newx;
		self['y']=newy;
		if smooth==1:
			Dx=(xmax-xmin)/20;
			dx=Dx/2;
			self.smoothstep(xmin-Dx,xmin+Dx);
			self.smoothstep(xmax-Dx,xmax+Dx);
		
	def commonrange(self,spect):
		xmin=max(min(self['x']),min(spect['x']));
		xmax=min(max(self['x']),max(spect['x']));
		return (xmin,xmax)
		
	def mapx(self,standardspect):
		spect=standardspect.copyxy();
		spect1=self.copyxy();
		spect1.addshoulder();
		xint=spect1['x'];
		yint=spect1['y'];
		ints=scipy.interpolate.interp1d(xint,yint);
		xnew=spect['x'];
		#print min(self['x']),max(self['x']);
		#print min(xnew),max(xnew);
		ynew=ints(xnew);
		self['x']=xnew;
		self['y']=ynew;

	def getcommonxy(self,spect1,xmin=None,xmax=None):
		self.sortx();
		spect1.sortx();
		if xmin is None:
			xmin=min(min(self['x']),min(spect1['x']));
		if xmax is None:
			xmax=max(max(self['x']),max(spect1['x']));
		I1=numpy.core.logical_and(self['x']>=xmin, self['x']<=xmax);
		I2=numpy.core.logical_and(spect1['x']>=xmin, spect1['x']<=xmax);
		if len(self['x'][I1])==0 or len(spect1['x'][I2])==0:
			x=None;
			y1=None;
			y2=None;
		else:
			#print "none zero"
			xlow=max(min(self['x'][I1]),min(spect1['x'][I2]));
			xhigh=min(max(self['x'][I1]),max(spect1['x'][I2]));
			N1=len(self['x'][I1]);
			N2=len(spect1['x'][I2]);
			N=max(N1,N2);
			dx=(xhigh-xlow)/N/2;
			#x=xarange(xlow,xhigh+dx,dx);
			#x=scipy.xarange(xlow,xhigh,2*N+1);
			#eps=self['xunit'].getcurrenttolerance();
			x=scipy.linspace(xlow,xhigh,2*N+1);
			#print xlow,xhigh,dx,len(x)
			selfext=self.copyxy();
			selfext.addshoulder();
			spect1ext=spect1.copyxy();
			spect1ext.addshoulder();
			int1=scipy.interpolate.interp1d(selfext['x'],selfext['y']);
			int2=scipy.interpolate.interp1d(spect1ext['x'],spect1ext['y']);
			#print "min max(x)",min(x),max(x)
			#print "min max x2",min(spect1ext['x']),max(spect1ext['x']);
			y1=int1(x);
			y2=int2(x);
		return (x,y1,y2);
	
#==========================================================================
# pure functions
#==========================================================================
	def renormgain_chi2(self,gainfactor,y2gain,ystandard):
		check=numpy.core.maximum(numpy.core.fabs(ystandard),numpy.core.fabs(y2gain));
		yfit=y2gain*gainfactor;
		chi2=(numpy.power(yfit-ystandard,2)/check).sum();
		return chi2;
		
	def noneoverlap_renormgain_chi2(self,paras,xL,yL,xR,yR):
	# here xR and yR times a gainfactor will fit the same polynomial as xL and yL
		gainfactor=paras[0];
		P=paras[1:];
		yfitL=numpy.polyval(P,xL);
		checkL=numpy.core.maximum(numpy.core.fabs(yL),numpy.core.fabs(yfitL));
		yfitR=numpy.polyval(P,xR)/gainfactor;
		checkR=numpy.core.maximum(numpy.core.fabs(yR),numpy.core.fabs(yfitR));
		chi2L=(numpy.power(yfitL-yL,2)/checkL).sum();
		chi2R=(numpy.power(yfitR-yR,2)/checkR).sum();
		chi2=chi2L+chi2R;
		return chi2;
		
	def renormshift_chi2(self,shift,y2gain,ystandard):
		check=numpy.core.maximum(numpy.core.fabs(ystandard),numpy.core.fabs(y2gain));
		yfit=y2gain+shift;
		chi2=(numpy.power(yfit-ystandard,2)/check).sum();
		return chi2
		
	def renormramp_chi2(self,paras,x,y2gain,ystandard):
		#gainfactor=paras[0];
		#shift=paras[1];
		#print "shift and gain:",paras
		check=numpy.core.maximum(numpy.core.fabs(ystandard),numpy.core.fabs(y2gain));
		yfit=y2gain*(paras[0]+paras[1]*x);
		chi2=(numpy.power(yfit-ystandard,2)/check).sum();
		return chi2
		
	def renormrampshift_chi2(self,paras,x,y2gain,ystandard):
		#gainfactor=paras[0];
		#shift=paras[1];
		#print "shift and gain:",paras
		check=numpy.core.maximum(numpy.core.fabs(ystandard),numpy.core.fabs(y2gain));
		yfit=y2gain*(paras[0]+paras[1]*x)+paras[2];
		chi2=(numpy.power(yfit-ystandard,2)/check).sum();
		return chi2

	def renormboth_chi2(self,paras,y2gain,ystandard):
		gainfactor=paras[0];
		shift=paras[1];
		#print "shift and gain:",paras
		check=numpy.core.maximum(numpy.core.fabs(ystandard),numpy.core.fabs(y2gain));
		yfit=y2gain*gainfactor+shift;
		chi2=(numpy.power(yfit-ystandard,2)/check).sum();
		return chi2
		
	def gaussfit_baseslope_chi2(self,paras,x,y):
		#gainfactor=paras[0];
		#shift=paras[1];
		#print "shift and gain:",paras
		amp=paras[0];
		center=paras[1];
		sigma=paras[2];
		slope=paras[3];
		intercept=paras[4];
		
		yfit=amp*numpy.exp(-(x-center)**2/sigma**2/2)+slope*x+intercept;
		check=numpy.core.maximum(numpy.core.fabs(y),numpy.core.fabs(yfit));
		chi2=((yfit-y)**2/check).sum();
		return chi2
		
	def gaussfit_base_chi2(self,paras,x,y):
		#gainfactor=paras[0];
		#shift=paras[1];
		#print "shift and gain:",paras
		amp=paras[0];
		center=paras[1];
		sigma=paras[2];
		slope=0;
		intercept=paras[3];
		
		yfit=amp*numpy.exp(-(x-center)**2/sigma**2/2)+slope*x+intercept;
		check=numpy.core.maximum(numpy.core.fabs(y),numpy.core.fabs(yfit));
		chi2=((yfit-y)**2/check).sum();
		return chi2
		
	def gaussfit_chi2(self,paras,x,y):
		#gainfactor=paras[0];
		#shift=paras[1];
		#print "shift and gain:",paras
		amp=paras[0];
		center=paras[1];
		sigma=paras[2];
		slope=0#paras[3];
		intercept=0#paras[4];
		
		yfit=amp*numpy.exp(-(x-center)**2/sigma**2/2)+slope*x+intercept;
		check=numpy.core.maximum(numpy.core.fabs(y),numpy.core.fabs(yfit));
		chi2=((yfit-y)**2/check).sum();
		return chi2
	
	def expdecayfit_chi2(self,paras,x,y):
		I0=paras[0];
		tau=paras[1];
		baseline=paras[2];
		
		yfit=I0*numpy.exp(-x/tau)+baseline;
		check=numpy.core.maximum(numpy.core.fabs(y),numpy.core.fabs(yfit));
		#check=1;
		chi2=((yfit-y)**2/check).sum();
		#chi2=((yfit-y)**2).sum();
		return chi2;
		
	def contextmenu(self,menu,dataname=''):
		import time,os;
		topmaster=gettoplevelmaster(menu);
		
		menu=DataObject.__dict__['contextmenu'](self,menu);
		menu.add_separator();
		menu.add_command(label="Setxy",command=lambda:self.uisetxy());
		menu.add_command(label="Summary",command=lambda:self.summarize(topmaster));
		return menu;
	
	def uisetxy(self):
		xexpression=self.get('xexpression');
		yexpression=self.get('yexpression');
		if xexpression is None:
			xexpression='numpy.arange(0,100,1)';
		if yexpression is None:
			yexpression='x';
		msg="Enter the field\n";
		msg=msg+"e.g.\n" 
		msg=msg+"x=numpy.arange(0,100,1)\n";
		msg=msg+"y=pylab.log(y)\n";
		answers=easygui.multenterbox(msg,"Setting x y",['x=','y='],[xexpression,yexpression]);
		if answers is not None:
			x=self['x'];
			y=self['y'];
			if answers[0] is not None:
				xexpression=answers[0];
			if answers[1] is not None:
				yexpression=answers[1];
			x=eval(xexpression);
			y=eval(yexpression);
			self['x']=x;
			self['y']=y;
			self['xexpression']=xexpression;
			self['yexpression']=yexpression;
			
	def summarize(self,topmaster=None):
		x=self['x'];
		summary=dict();
		summary['len']=len(x);
		xc=x.copy();
		xc.sort();
		difx=numpy.diff(xc);
		summary['xunit']=self['xunit']['currentunit'];
		summary['res_min']=min(difx);
		summary['res_max']=max(difx);
		summary['res_mean']=numpy.mean(difx);
		if topmaster is not None:
			topmaster.stdout( summary);
		return summary;
		#self['summary']=summary;