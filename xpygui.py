# this is to set the path and reload everything
import os;
import sys;	
import time;

def setpath():
	import os,sys;
	abspath=os.path.abspath(os.curdir)
	addpath(abspath);
	files=os.listdir(os.curdir);
	for file in files:
		fullname=os.path.join(os.curdir, file);
		if os.path.isdir(fullname) and file[0]!='#':
			setsubpath(fullname);
	return abspath;

def setsubpath(dirname):
	#print 'in dir: ', dirname
	dirname=os.path.abspath(dirname);
	#sys.path.insert(1,dirname);
	addpath(dirname);
	files=os.listdir(dirname);
	for file in files:
		fullname=os.path.join(dirname, file);
		if os.path.isdir(fullname) and file[0]!='#':
			setsubpath(fullname);
			
def addpath(abspathstr):
	pathlist=sys.path;
	I=None;
	if pathlist.count(abspathstr)==0:
		sys.path.insert(1,abspathstr);
	
	
t=time.time();
abspath=setpath();
#print "rootpath:",abspath
import xos;
libpath=os.path.join(abspath,"lib");
x=xos.XOS(libpath);
x.reloadallxpymods();
print len(x['importstack']),"modules imported."
print "It took ",time.time()-t,'seconds'
