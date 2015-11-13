from dataobject import *;
from units import *;
from xpyfun import *;
from xos import *;
from xydiscretefun import *;
import pylab;
import scipy.interpolate;
import scipy.optimize;
import scipy;
import numpy;
import copy;
import os;
import scipy;

class XyzDiscreteFun(XyDiscreteFun):
	def __init__(self):
		XyDiscreteFun.__dict__['__init__'](self);
		self['zunit']=Units();

	def sortxy(self):
		x = self['x'];
		y = self['y'];
		z = self['z'];

		I=numpy.argsort(x);
		x=x[I];
		z=z[:,I];
		I=numpy.argsort(y);
		y=y[I];
		z=z[I,:];
		
		self['x']=x;
		self['y']=y;
		self['z']=z;