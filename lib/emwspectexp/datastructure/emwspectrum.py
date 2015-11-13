from spectraunits import *;
from dimlessunits import *;
from optcondunits import *;
from absorbanceunits import *;
from numdatasheetplotable import *;
import pylab;
import numpy;

class EMWSpectrum(NumDataSheetPlotable):
	def __init__(self,filename=None,dilimiter="\t",row_width_chosen=None):
		NumDataSheetPlotable.__dict__['__init__'](self,filename,dilimiter,row_width_chosen);
		self.set('xunit',SpectraUnits());
		self['Temperature']=300;
		self['Mag_Field']=0;
		self['Polarization']=0;

	def phaseshifts(self,efree,alpha,lowmethod,statuslabel=None):
		import time;
		xnew=[];
		ynew=[];
		L=len(self['x']);
		t0=time.time();
		for i in range(1,L-1):
			x0=self['x'][i];
			y0=self['y'][i];
			yshift=self.phaseshiftx0(x0,y0,efree,alpha,lowmethod);
			xnew.append(x0);
			ynew.append(yshift);
			
			t1=time.time();
			if t1-t0>2:
				print "Finished:",float(i)/L*100,'%',"nu:",x0;
				t0=t1;
		spectnew=self.copyxy();
		spectnew['x']=numpy.array(xnew);
		spectnew['y']=numpy.array(ynew);
		return spectnew;
		
	def phaseshiftx0(self,x0,y0,efree,alpha,lowmethod):
		# for low energy part
		x=self['x'];
		y=self['y'];
		if lowmethod=="constant":
			Nlow=100;
			dxlow=x[0]/Nlow;
			xlow=numpy.arange(0,x[0],dxlow);
			ylow=xlow-xlow+y[0];
			numerator=numpy.log(ylow)-numpy.log(y0);
			denominator=numpy.power(x0,2)-numpy.power(xlow,2);
			Intlow=(numerator/denominator*dxlow).sum();
		else:
			Intlow=0;

		# for interband
		Ninter=100;
		dxinter=(efree-x[-1])/Ninter;
		xinterband=numpy.arange(x[-1]+dxinter,efree,dxinter);
		epower=alpha;
		C=y[-1]/numpy.power(x[-1],epower);
		yinterband=C*numpy.power(xinterband,epower);
		numerator=numpy.log(yinterband)-numpy.log(y0);
		#for an ossillator at 10eV
		pos=10*1e7/1240;
		width=1e7/1240;
		amp=0.9;
		amp=0;
		numeratorpeak=exp(-(pos-xinterband)**2/width**2/2)*amp;
		numerator=numerator+numeratorpeak;
		denominator=x0*x0-numpy.power(xinterband,2);
		Intinterband=(numerator/denominator*dxinter).sum();

		#% for free electron
		epower=-4;
		Nfree=100;
		dxfreeelectron=efree/Nfree;
		xfreeelectron=numpy.arange(efree,efree*4,dxfreeelectron);
		C=yinterband[-1]/numpy.power(xinterband[-1],epower);
		yfreeelectron=C*numpy.power(xfreeelectron,epower);
		numerator=numpy.log(yfreeelectron)-numpy.log(y0);
		denominator=x0*x0-numpy.power(xfreeelectron,2);
		Intfreeelectron=(numerator/denominator*dxfreeelectron).sum();

		#% for experimental data
		numerator=numpy.log(y)-numpy.log(y0);
		denominator=x0*x0-x*x;
		I=(numpy.fabs(denominator)<1e-10);
		IL=numpy.hstack((I[1:],[False]));
		IR=numpy.hstack(([False],I[0:-1]));
		#numerator[I]=(numpy.log(y[IR])-numpy.log(y[I]))/(x[IR]-x[I]);
		#denominator[I]=-2*x0;
		numerator[I]=(numpy.log(y[IR])-numpy.log(y[I]))/(x[IR]-x[I]);
		denominator[I]=-2*x[I];
		Intexp=(numerator[0:-1]/denominator[0:-1]*numpy.diff(x)).sum();

		shift=x0/numpy.pi*(Intlow+Intexp+Intinterband+Intfreeelectron);
		return shift;
		
	def spectphaseshifts(self,efree,alpha,lowmethod,statuslabel=None):
		import time;
		
		spectext=self.copyxy();
		spectext.extendspect4phaseshift(efree,alpha,lowmethod);
		#figure();
		#spectext.plot('o');
		#pylab.gca().set(xscale='log');
		#pylab.gca().set(yscale='log');
		
		spectnew=self.copyxy();
		x=spectnew['x'];
		ynew=spectnew['y'];
		
		t0=time.time();
		L=len(x);
		for i in range(L):
			x0=x[i];
			yshift=spectext.phaseshiftx0NE(x0);
			ynew[i]=yshift;
			
			t1=time.time();
			if t1-t0>2:
				print "Finished:",float(i)/L*100,'%',"nu:",x0;
				t0=t1;
		spectnew['y']=ynew;
		return spectnew;
		
	def extendspect4phaseshift(self,efree,alpha,lowmethod):
		# for low energy part
		x=self['x'];
		y=self['y'];
		Nlow=100;
		if lowmethod=="constant":
			dxlow=x[0]/Nlow;
			xlow=numpy.arange(0,x[0],dxlow);
			ylow=xlow-xlow+y[0];
		else:
			xlow=array([0]);
			ylow=array(y[0]);

		# for interband
		Ninter=100;
		dxinter=(efree-x[-1])/Ninter;
		xinterband=numpy.arange(x[-1]+dxinter,efree,dxinter);
		epower=alpha;
		C=y[-1]/numpy.power(x[-1],epower);
		yinterband=C*numpy.power(xinterband,epower);
		#numerator=numpy.log(yinterband)-numpy.log(y0);
		#for an ossillator at 10eV
		pos=10*1e7/1240;
		width=1e7/1240;
		amp=0.9;
		amp=0;
		yinterbandpeak=exp(-(pos-xinterband)**2/width**2/2)*amp;
		yinterband=yinterband+yinterbandpeak;

		#% for free electron
		Nfree=100;
		epower=-4;
		dxfreeelectron=efree/Nfree;
		xfreeelectron=numpy.arange(efree,efree*4,dxfreeelectron);
		C=yinterband[-1]/numpy.power(xinterband[-1],epower);
		yfreeelectron=C*numpy.power(xfreeelectron,epower);

		#% combine everythin together
		x=numpy.hstack((xlow,x,xinterband,xfreeelectron));
		y=numpy.hstack((ylow,y,yinterband,yfreeelectron));
		self['x']=x;
		self['y']=y;
		#print len(x),len(set(x))
		
	def phaseshiftx0NE(self,x0):
		x=self['x'];
		y=self['y'];
		y0=self(x0);
		numerator=numpy.log(y)-numpy.log(y0);
		denominator=x0*x0-x*x;
		I=(numpy.fabs(denominator)<1e-10);
		#IL=numpy.hstack((I[1:],[False]));
		IR=numpy.hstack(([False],I[0:-1]));
		#numerator[I]=(numpy.log(y[IR])-numpy.log(y[I]))/(x[IR]-x[I]);
		#denominator[I]=-2*x0;
		numerator[I]=(numpy.log(y[IR])-numpy.log(y[I]))/(x[IR]-x[I]);
		denominator[I]=-(x[IR]**2-x[I]**2)/(x[IR]-x[I]);
		#print numerator[I]
		#print denominator[I]
		shiftfunc=numerator[0:-1]/denominator[0:-1];
		shift=x0/numpy.pi*(shiftfunc*numpy.diff(x)).sum();
		#print shiftfunc.sum()
		#print diff(x).sum()
		return shift;
	
	def optfncs(self,spectphaseshift):
		#print "len",len(self['x']),len(spectphaseshift['x'])
		spect=self.copyxy();
		spect.mapx(spectphaseshift);
	
		x=spectphaseshift['x'];
		yrfl=spect['y'];
		yphase=spectphaseshift['y'];
		
		roucostheta=numpy.sqrt(yrfl)*numpy.cos(yphase);
		
		yn=(1-yrfl)/(1-2*roucostheta+yrfl);
		yk=numpy.sqrt((yrfl*(yn+1)*(yn+1)-(yn-1)*(yn-1))/(1-yrfl));
		sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha=spect.nk2allopts(yn,yk);
		return (sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha);
		
	def finddirectgap(self,xmin=None,xmax=None):
		# assuming this spectrum is absorption coefficient
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		spect['y']=numpy.power(spect['y']*spect['x'],2);
		(P,dy)=spect.polyfit(1);
		gap=-P[1]/P[0];
		gaperr=dy/P[0];
		#self.log({"method":"finddirectgap","xmin":xmin,"xmax":xmax});
		return (gap,P,spect,gaperr);
		
	def findindirectgap(self,xmin=None,xmax=None):
		# assuming this spectrum is absorption coefficient
		spect=self.copyxy();
		spect.pick(xmin,xmax);
		spect['y']=numpy.sqrt(spect['y']*spect['x']);
		(P,dy)=spect.polyfit(1);
		gap=-P[1]/P[0];
		gaperr=dy/P[0];
		#self.log({"method":"findindirectgap","xmin":xmin,"xmax":xmax});
		return (gap,P,spect,gaperr);
		
	def contextmenu(self,menu,dataname=''):
		menu=NumDataSheetPlotable.contextmenu(self,menu,dataname);
		return menu;
		
	def sumrule(self,V0,xmin=None,xmax=None):
		e=1.6e-19;
		m=9.1e-31;
		epsilon0=1./4./numpy.pi/9e9;
		omegap2=e**2/V0/m/epsilon0;
		#print "omegap",sqrt(omegap2)
		
		spect0=self.copyxy();
		spect0.pick(xmin,xmax);
		x=spect0['x'];
		y=spect0['y'];
		
		xomega=2*numpy.pi*3e8*x*1e2;
		neff0=self['y'][0]*xomega[0];
		neff0=0;
		neff=xomega-xomega;
		for i in range(len(xomega)):
			if i==0:
				neff[i]=neff0;
			else:
				neff[i]=neff[i-1]+xomega[i]*y[i]*(xomega[i]-xomega[i-1]);
		spect=spect0.copyxy();
		spect['y']=neff/omegap2/pi*2;
		return (spect,sqrt(omegap2))
		
	def optfuncsfromRT(self,spectTrans,d):
		import mathfunc as m;
		import time;
		x=self['x'];
		xomega=2*numpy.pi*3e8*x*1e2;
		R=self['y'];
		T=spectTrans['y'];
		yn=R.copy();
		yk=R.copy();
		ychi2=R.copy();
		
		t1=time.time();
		for i in range(len(xomega)):
			omegat=xomega[i];
			n,k,chi2=m.nkslabNI(R[i],T[i],d,omegat);
			yn[i]=n;
			yk[i]=k;
			ychi2[i]=chi2;
			t=time.time();
			if t-t1>2:
				print "Finished:",float(i)/len(xomega)*100,'%',"nu:",x[i];
				t1=t;
		sp_chi2=self.copyxy();
		sp_chi2['y']=ychi2;
		
		sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha=self.nk2allopts(yn,yk);
		
		return (sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha,sp_chi2);

	def optfuncsfromRTFilm(self,spectTrans,d,spectnsub,spectksub,dsub):
		import mathfunc as m;
		import time;
		x=self['x'];
		xomega=2*numpy.pi*3e8*x*1e2;
		R=self['y'];
		T=spectTrans['y'];
		ynsub=spectnsub['y'];
		yksub=spectksub['y'];
		yn=R.copy();
		yk=R.copy();
		ychi2=R.copy();
		
		t1=time.time();
		for i in range(len(xomega)):
			omegat=xomega[i];
			n,k,chi2=m.nkfilmNI(R[i],T[i],d,ynsub[i],yksub[i],dsub,omegat);
			yn[i]=n;
			yk[i]=k;
			ychi2[i]=chi2;
			t=time.time();
			if t-t1>2:
				print "Finished:",float(i)/len(xomega)*100,'%',"nu:",x[i];
				t1=t;
		sp_chi2=self.copyxy();
		sp_chi2['y']=ychi2;
		
		sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha=self.nk2allopts(yn,yk);
		
		return (sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha,sp_chi2);

		
	def nk2allopts(self,yn,yk):
		spect=self;
		x=spect['x'];
		
		yepsilon1=yn*yn-yk*yk;
		yepsilon2=2*yn*yk;

		epsilon0=1./4./numpy.pi/9e9;
		xomega=2*numpy.pi*3e8*x*1e2;
		#ysigma=yepsilon2/4/numpy.pi*xomega*epsilon0;
		ysigma=yepsilon2*xomega*epsilon0;
		#yalpha=4*numpy.pi*ysigma/yn/3e8/epsilon0;
		yalpha=ysigma/yn/3e8/epsilon0;
		
		sp_n=spect.copyxy();
		sp_n['y']=yn;
		sp_n['yunit']=DimlessUnits('n');
		
		sp_k=spect.copyxy();
		sp_k['y']=yk;
		sp_k['yunit']=DimlessUnits('k');
		
		sp_epsilon1=spect.copyxy();
		sp_epsilon1['y']=yepsilon1;
		sp_epsilon1['yunit']=DimlessUnits('\epsilon_1');
		
		sp_epsilon2=spect.copyxy();
		sp_epsilon2['y']=yepsilon2;
		sp_epsilon2['yunit']=DimlessUnits('\epsilon_2');
		
		sp_sigma=spect.copyxy();
		sp_sigma['y']=ysigma;
		sp_sigma['yunit']=OptCondUnits();
		
		sp_alpha=spect.copyxy();
		sp_alpha['y']=yalpha;
		sp_alpha['yunit']=AbsorbanceUnits();
		
		#sp_sigma.plot();
		#sp_alpha.plot();
		return (sp_n,sp_k,sp_epsilon1,sp_epsilon2,sp_sigma,sp_alpha);

	def pelletfit(self,spectXystal):
		import mathfunc as m;
		yXystal=spectXystal['y'];
		ypellet=self['y'];
		dratio,ratio,shift,chi2=m.pelletfit(ypellet,yXystal);
		spect=self.copyxy();
		ynew=((spect['y']-shift)/ratio)**(1/dratio);
		spect['y']=ynew;
		return (spect,dratio,ratio,shift,chi2);
		
	def alpha2color(self,thickness,brightness=1,normalize=True):
		import mathfunc as m;
		R=0.;
		G=0.;
		B=0.;
		for wl in range(380,781):
			nu=1e7/wl;
			alpha=self(nu);
			if alpha is not None:
				trans=exp(-alpha*thickness);
			#print "alpha,thickness,trans",alpha,thickness,trans
				r,g,b=m.wavelength2rgb(wl);
			#print "r,g,b",r,g,b
				R=R+r*trans/(780.-380)/256.*brightness;
				G=G+g*trans/(780.-380)/256.*brightness;
				B=B+b*trans/(780.-380)/256.*brightness;
		if normalize:	
			R=min(R,1.);
			G=min(G,1.);
			B=min(B,1.);
		return (R,G,B);
			