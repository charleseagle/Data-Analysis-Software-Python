import numpy;
from pylab import *;
import numpy;
import scipy.optimize as opt;

thetarange=arange(0,2*pi,pi/32);
theta2,theta3=meshgrid(thetarange,thetarange);
#theta2=0;

def refr(r1,r2,NR):
	A=[1];
	for N0 in range(NR-1):
		N=N0+1;
		Atemp=(1-r1)**2*(r2/r1)*(r1*r2)**(N-1);
		A.append(Atemp);
	return A;
	
def refint(WL,n,d,r1,r2,NR):
	A=refr(r1,r2,NR);
	B=(r1/r2)**2;
	Int=WL-WL;
	for N1 in range(NR):
		for N2 in range(NR):
			Int=Int+A[N1]*A[N2]*cos(4*(N1-N2)*pi*n*d/WL);
		#(1+A1*cos(4*pi*n*d/WL)+A2*cos(8*pi*n*d/WL))**2*B/Int0;
	Int=Int*B;
	return Int;
	
def doublereflectionratio(wavelength,filmthickness,rfilm,rsample):
	
	NR=5;
	nfilm=2/(1-rfilm)-1;
	nsample=2/(1-rsample)-1;
	r1=rfilm;
	r2=numpy.fabs(nsample-nfilm)/(nsample+nfilm);
	
	A=[1];
	for N0 in range(NR-1):
		N=N0+1;
		Atemp=(1-r1)**2*(r2/r1)*(r1*r2)**(N-1);
		A.append(Atemp);

	B=(r1/r2)**2;
	WL=wavelength;
	d=filmthickness;
	n=nfilm;
	
	Int0=refint(WL,n,0,r1,r2,NR);
	Int=refint(WL,n,d,r1,r2,NR);
	Int=Int/Int0;
	return Int;
	

def fzero(f,xmin,xmax,eps=1e-5,Nmax=500):
	x=float(xmin+xmax)/2.0;
	y=f(x);
	N=0;
	while abs(y)>eps and N<Nmax:
		if y*f(xmin)>0:
			xmin=x;
			x=(x+xmax)/2.0;
		else:
			xmax=x;
			x=(x+xmin)/2.0;
		N=N+1;
		y=f(x);
	if N==Nmax:
		print "Max iteration exceeded, y:",y
	return x;
	
def localmins(ys):
	yc=ys[1:-1];
	yl=ys[:-2];
	yr=ys[2:];
	I=logical_and(yc<yl,yc<yr);
	I=numpy.hstack((False,I,False));
	return I;
	
def find1stminfilmthickness(wavelength,rfilm,rsample):
	drange=linspace(0,wavelength/4,500);
	ys=doublereflectionratio(wavelength,drange,rfilm,rsample);
	I=localmins(ys);
	dmin=drange[I];
	return dmin;
	
def findfilmthickness(yratio,wavelength,rfilm,rsample):
	dmin=0;
	#dmax=wavelength/5;
	dmax=find1stminfilmthickness(wavelength,rfilm,rsample);
	#print "dmax",dmax/wavelength;
	
	f=lambda d:doublereflectionratio(wavelength,d,rfilm,rsample)-yratio;
	#drange=linspace(dmin,dmax,100);
	#plot(drange,f(drange));grid(True);
	#d=opt.fsolve(f,dmin,dmax);
	d=opt.fsolve(f,(dmin+dmax)/2);
	return d;
	
def findrsample(yraw,wavelength,filmthickness,rfilm):
	ymin=0.;
	ymax=1-1e-5;
	d=filmthickness;
	f=lambda ysample:ysample*doublereflectionratio(wavelength,d,rfilm,ysample**0.5)-yraw;
	#rsample=opt.fsolve(f,rmin,rmax);
	ysample=opt.fsolve(f,(ymin+ymax)/2);
	#yrange=linspace(ymin,ymax,100);
	#plot(rrange,f(rrange));grid(True);
	#plot(yrange,doublereflectionratio(wavelength,d,rfilm,yrange**0.5));grid(True);
	#print "rraw/rsample:",rraw/rsample
	return ysample;

#==========================
# for Glover Tinkham analysis
#==========================
def RTslab(n,k,x,omegat):
	c=3e8;
	Rs=((1-n)**2+k**2)/((1+n)**2+k**2);
	alpha=2*omegat*k/c;
	beta=n*omegat*x/c;
	tanphi=2*k/(k**2+n**2-1);
	sinphi2=1/(1+1/tanphi**2);
	cosphi2=1/(1+tanphi**2);
	sinphibeta2=sinphi2*cos(beta)**2+cosphi2*sin(beta)**2+2*cosphi2*tanphi*sin(beta)*cos(beta);
	A=exp(-alpha*x);
	
	Tnum=((1-Rs)**2+4*Rs*sinphi2)*A;
	Tden=(1-Rs*A)**2+4*Rs*A*sinphibeta2;
	
	Rnum=(1-A)**2+4*A*sinphibeta2;
	
	T=Tnum/Tden;
	R=Rnum*Rs/Tden;
	#print Rs,alpha,tanphi
	#print Tnum,Tden
	#print Rs,Rnum
	#print "n:",n,"k:",k
	#print "R:",R,"T:",T
	return (R,T);

def chisRTslab(paras,R,T,x,omegat):
	n,k=paras;
	Rfit,Tfit=RTslab(n,k,x,omegat);
	gain=1.;
	chi=((R-Rfit)*gain,(log(T)-log(Tfit))*gain);
	return chi;

def nkslab(R,T,x,omegat):
	n0,k0,chi20=nkslabNI(R,T,x,omegat);
	paras=opt.leastsq(chisRTslab,(n0,k0),args=(R,T,x,omegat));
	
	n=paras[0][0];
	k=paras[0][1];
	chi=chisRTslab((n,k),R,T,x,omegat)
	chi2=(array(chi)**2).sum();
	Rfit,Tfit=RTslab(n,k,x,omegat);
	#print "paras:",paras
	#print "n:",n,"k:",k
	#print "chi:",chi,"chi2:",chi2
	#print "Rfit:",Rfit,"R:",R
	#print "Tfit:",Tfit,"T:",T
	return (n,k,chi2);
	
def RTslabNI(n,k,x,omegat):
	c=3e8;
	Rs=((1-n)**2+k**2)/((1+n)**2+k**2);
	alpha=2*omegat*k/c;
	A=exp(-alpha*x);
	
	Tnum=(1-Rs)**2*A;
	Tden=1-(Rs*A)**2;
	
	Rnum=1+(1-2*Rs)*A**2;
	
	T=Tnum/Tden;
	R=Rnum*Rs/Tden;
	#if R<0 or T<0:
	#	print "n,k:",n,k
	return (R,T);
	
def chisRTslabNI(paras,R,T,x,omegat):
	n,k=paras;
	Rfit,Tfit=RTslabNI(n,k,x,omegat);
	gain=1.;
	chi=((R-Rfit)*gain,(log(T)-log(Tfit))*gain);
	return chi;

def nkslabNI(R,T,x,omegat):
	c=3e8;
	k0=-log(T)/x*c/2/omegat;
	b=2-4/(1-R);
	c=1+k0**2;
	n0=(-b+sqrt(abs(b**2-4*c)))/2;
	
	paras0=(n0,k0);
	paras=opt.leastsq(chisRTslabNI,paras0,args=(R,T,x,omegat));
	
	n=paras[0][0];
	k=paras[0][1];
	chi=chisRTslabNI((n,k),R,T,x,omegat)
	chi2=(array(chi)**2).sum();
	Rfit,Tfit=RTslabNI(n,k,x,omegat);
	#print "paras:",paras
	#print "n:",n,"k:",k
	#print "chi:",chi,"chi2:",chi2
	#print "Rfit:",Rfit,"R:",R
	#print "Tfit:",Tfit,"T:",T
	return (n,k,chi2);
	

#=============================
#3 layer Glover Tinkham Analysis
#=============================
def t_ij(Ni,Nj):
	t=2*Ni/(Ni+Nj);
	return t;
	
def r_ij(Ni,Nj):
	r=(Ni-Nj)/(Ni+Nj);
	return r;
	
def a_i(N,x,omegat,theta=0):
	c=3e8;
	j=complex(0,1);
	A=exp((theta+N*omegat*x/c)*j);
	return A;
	
def b_ijk(N1,N2,N3,x2,omegat,theta=0):
	A2=a_i(N2,x2,omegat,theta);
	r23=r_ij(N2,N3);
	r21=r_ij(N2,N1);
	B=1/(1-A2**2*r23*r21);
	return B;
	
def bbetween(Ns,xs,omegat,thetas=None):
	r0=r_ij(Ns[1],Ns[0]);
	r_1=r_ij(Ns[-2],Ns[-1]);
	b=r0*r_1;
	for i in range(len(Ns)-2):
		j=i+1;
		#print type(thetas)
		if thetas is None:
			theta=0;
		else:
			theta=thetas[i];
		aj=a_i(Ns[j],xs[i],omegat,theta);
		b=b*aj**2;
	for i in range(len(Ns)-3):
		j=i+1;
		tj=t_ij(Ns[j],Ns[j+1])*t_ij(Ns[j+1],Ns[j]);
		b=b*tj;
	B=1/(1-b);
	return B;
	
def RTfilm(n2,k2,x2,n3,k3,x3,omegat,theta2=0,theta3=0):
	c=3e8;
	N1=complex(1);
	N2=complex(n2,k2);
	N3=complex(n3,k3);
	N4=complex(1);
	j=complex(0,1);
	
	A2=a_i(N2,x2,omegat,theta2);
	A3=a_i(N3,x3,omegat,theta3);
	
	B123=bbetween((N1,N2,N3),[x2],omegat,[theta2]);
	B234=bbetween((N2,N3,N4),[x3],omegat,[theta3]);
	B1234=bbetween((N1,N2,N3,N4),(x2,x3),omegat,(theta2,theta3));
	
	t12=t_ij(N1,N2);
	t21=t_ij(N2,N1);
	t23=t_ij(N2,N3);
	t34=t_ij(N3,N4)
	t32=t_ij(N3,N2)

	r12=r_ij(N1,N2);
	r23=r_ij(N2,N3);
	r34=r_ij(N3,N4)
	
	tf=t12*A2*t23*A3*t34*B123*B234*B1234;
	rf=r12;
	rf=rf+t12*A2*r23*A2*t21*B123;
	rf=rf+t12*A2*t23*A3*r34*A3*t32*A2*t21*B123*B234*B1234;
	
	T=mean(abs(tf)**2);
	R=mean(abs(rf)**2);
	#print "r12:",abs(r_ij(N1,N2)),"r23",abs(r_ij(N2,N3)),"r34:",abs(r_ij(N3,N4))	
	#print "t12:",abs(t_ij(N1,N2)),"t23",abs(t_ij(N2,N3)),"t34:",abs(t_ij(N3,N4))
	#print "A2:",abs(A2),"A3:",abs(A3)
	#print "B2:",abs(B2),"B3:",abs(B3)
	return (R,T)

def chisRTfilm(paras,R,T,x2,n3,k3,x3,omegat):
	n2,k2=paras;
	Rfit,Tfit=RTfilm(n2,k2,x2,n3,k3,x3,omegat);
	#RTfilm(n,k,x,omegat);
	gain=1.;
	chi=((R-Rfit)*gain,(log(T)-log(Tfit))*gain);
	return chi;

def nkfilm(R,T,x2,n3,k3,x3,omegat):
	c=3e8;
	k0=-log(T)/x2*c/2/omegat;
	b=2-4/(1-R);
	c=1+k0**2;
	n0=(-b+sqrt(abs(b**2-4*c)))/2;
	
	paras0=(n0,k0);
	paras=opt.leastsq(chisRTfilm,paras0,args=(R,T,x2,n3,k3,x3,omegat));
	
	n2=paras[0][0];
	k2=paras[0][1];
	chi=chisRTfilm((n2,k2),R,T,x2,n3,k3,x3,omegat)
	chi2=(array(chi)**2).sum();
	#Rfit,Tfit=RTfilm(n,k,x,omegat);
	#print "paras:",paras
	#print "n:",n,"k:",k
	#print "chi:",chi,"chi2:",chi2
	#print "Rfit:",Rfit,"R:",R
	#print "Tfit:",Tfit,"T:",T
	return (n2,k2,chi2);

"""def RTfilmNI(n2,k2,x2,n3,k3,x3,omegat):
	c=3e8;
	N1=complex(1);
	N2=complex(n2,k2);
	N3=complex(n3,k3);
	N4=complex(1);
	j=complex(0,1);

	t12=2*N1/(N1+N2);
	t21=2*N2/(N1+N2);
	t23=2*N2/(N2+N3);
	t32=2*N3/(N3+N2);
	t34=2*N3/(N3+N4);

	r12=(N1-N2)/(N1+N2);
	r21=(N2-N1)/(N1+N2);
	r23=(N2-N3)/(N2+N3);
	r32=(N3-N2)/(N3+N2);
	r34=(N3-N4)/(N3+N4);
	
	A2=exp((theta2+N2*omegat*x2/c)*j);
	A3=exp((theta3+N3*omegat*x3/c)*j);
	B2=1/(1-A2**2*r23*r21);
	B3=1/(1-A3**2*r34*r32);
	
	tf=t12*A2*B2*t23*A3*B3*t34;
	rf=r12+t12*A2*B2*r23*A2*B2*t21;
	rf=rf+t12*A2*B2*t23*A3*B3\
		*r34*A3*B3*t32*A2*B2*t21;
	
	T=mean(abs(tf)**2);
	R=mean(abs(rf)**2);

	#print "r12:",abs(r_ij(N1,N2)),"r23",abs(r_ij(N2,N3)),"r34:",abs(r_ij(N3,N4))	
	#print "t12:",abs(t_ij(N1,N2)),"t23",abs(t_ij(N2,N3)),"t34:",abs(t_ij(N3,N4))
	#print "A2:",abs(A2),"A3:",abs(A3)
	#print "B2:",abs(B2),"B3:",abs(B3)
	return (R,T)
"""
def RTfilmNI(n2,k2,x2,n3,k3,x3,omegat):
	R,T=RTfilm(n2,k2,x2,n3,k3,x3,omegat,theta2,theta3);
	return (R,T);
	
def chisRTfilmNI(paras,R,T,x2,n3,k3,x3,omegat):
	c=3e8;
	n2,k2=paras;
	Rfit,Tfit=RTfilmNI(n2,k2,x2,n3,k3,x3,omegat);
	#RTfilm(n,k,x,omegat);
	gain=1;
	if n2<0 :# or k2<0:
		gain=1e10;
	
	T3=exp(-2*omegat*x3*k3/c);
	Rdiff=R-Rfit;
	if abs(T-Tfit)>abs(log(T)-log(Tfit)):
		Tdiff=T-Tfit;
	else:
		Tdiff=log(T)-log(Tfit);
		
	chi=(Rdiff*gain,Tdiff*gain);
	return chi;

def nkfilmNI(R,T,x2,n3,k3,x3,omegat,verbose=False):
	import time;
	t0=time.time();
	b=2-4/(1-R);
	c=1;
	n0=(-b+sqrt(abs(b**2-4*c)))/2;
	
	N1=complex(1,0);
	N2=complex(n0,0);
	N3=complex(n3,k3);
	N4=complex(1,0);
	
	t12=t_ij(N1,N2);
	#B123=b_ijk(N1,N2,N3,x2,omegat);
	#print "B123:",B123
	B123=bbetween((N1,N2,N3),[x2],omegat);
	#print "B123:",B123
	t23=t_ij(N2,N3);
	A3=a_i(N3,x3,omegat);
	#B234=b_ijk(N2,N3,N4,x3,omegat);
	B234=bbetween((N2,N3,N4),[x3],omegat);
	t34=t_ij(N3,N4);
	
	T3=abs(t12*B123*t23*A3*B234*t34)**2;
	#print "T,T3,T2:",T, T3,T/T3
	k0=-log(T/T3)/x2*3e8/2/omegat;
	#k01=-log(T)/x2*3e8/2/omegat;
	#print "omgat:",omegat,"x2:",x2,"T:",T,1/x2*c/2/omegat
	#print "k0s",k0,k01
	if not k0>0:
		k0=0;
	
	paras0=(n0,k0);
	paras=opt.leastsq(chisRTfilmNI,paras0,args=(R,T,x2,n3,k3,x3,omegat));
	
	n2=paras[0][0];
	k2=paras[0][1];
	chi=chisRTfilmNI((n2,k2),R,T,x2,n3,k3,x3,omegat);
	chi2=(array(chi)**2).sum();
	
	if verbose:
		print "Input------------"
		print 'R:%(R)5.2f, T:%(T)5.2e, x2:%(x2)5.2e,'%vars()
		print 'n3:%(n3)5.2f, k3:%(k3)5.2e, x3:%(x3)5.2e,'%vars()
		print 'omegat:%(omegat)5.2e, '% vars()
		print "Output-----------"
		print "n,k guessed:",n0,k0
		print "n,k found:",n2,k2
		print "chi2",chi2
		print "time taken:",time.time()-t0;
		print "-----------------"
		
	return (n2,k2,chi2);

def pelletfit(tPellet,tXystal):
	dratio0=1;
	ratio0=1;
	shift0=0;
	paras=opt.leastsq(chispellet,(dratio0,ratio0,shift0),args=(tPellet,tXystal));
	dratio=paras[0][0];
	ratio=paras[0][1];
	shift=paras[0][2];
	chis=chispellet((dratio,ratio,shift),tPellet,tXystal);
	chi2=(array(chis)**2).sum();
	return (dratio,ratio,shift,chi2);
	
def chispellet((dratio,ratio,shift),tPellet,tXystal):
	treal=ratio*(tXystal)**dratio;
	tfit=treal+shift;
	chi=tfit-tPellet;
	if tfit.max()>=1 or tfit.min()<=0:
		chi=chi*1e100;
	return chi;
	
def wavelength2rgb(wl):
	maxInt=255;
	gamma=0.8;
	red=0.
	green=0.
	blue=0.;
	if wl>=380 and wl<=439:
		red   = -(wl - 440) / (440.- 380);
		green = 0.0;
		blue  = 1.0;
		
	elif wl>=440 and wl<=489:
		red   = 0.0;
		green = (wl - 440) / (490. - 440);
		blue  = 1.0;
 
	elif wl>=490 and wl<=509:    
		red   = 0.0;
		green = 1.0;
		blue  = -(wl - 510) / (510. - 490)     

	elif wl>=510 and wl<=579:      
		red   = (wl - 510) / (580. - 510);
		green = 1.0;
		blue  = 0.0;      

	elif wl>=580 and wl<=644:      
		red   = 1.0;
		green = -(wl - 645) / (645. - 580);
		blue  = 0.0;
		
	elif wl>=645 and wl<=780:
		red   = 1.0;
		green = 0.0;
		blue  = 0.0;
	else:
		red   = 0.0;
		green = 0.0;
		blue  = 0.0
	
	if wl>=380 and wl<=419:
		factor = 0.3 + 0.7*(wl - 380) / (420. - 380);
	elif wl>=420 and wl<=700:
		factor = 1.0;
	elif wl>=701 and wl<=780:
		factor = 0.3 + 0.7*(780 - wl) / (780. - 700)
	else:
		factor = 0.0
		
	R = rgbadjust(red,   factor,maxInt,gamma);
	G = rgbadjust(green, factor,maxInt,gamma);
	B = rgbadjust(blue,  factor,maxInt,gamma);

	return (R,G,B);
	
def rgbadjust(color,factor,maxInt,gamma):
	if color==0:
		result= 0.
	else:
		result=round(maxInt*(color*factor)**gamma);
	return result;
	
	