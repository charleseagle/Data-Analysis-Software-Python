import os;
import re;
class XOS(dict):
	importedmodnames=[];
	def __init__(self,rootpath=None):
		if rootpath is None:
			rootpath=os.path.abspath(os.path.curdir);
		self['rootpath']=rootpath;
		self['importstack']=[];
		
	def find(self,fname,abspname=None):
		foundabspathlist=[];
		if abspname is None:
			abspname=self['rootpath'];
		files=os.listdir(abspname);
		for file in files:
			fullname=os.path.join(abspname, file);
			#print "fullname:",fullname
			if os.path.isdir(fullname) and file[0]!='#':
				foundabspathl=self.find(fname,fullname);
				#print "foundabspathl",foundabspathl
				foundabspathlist=foundabspathlist+foundabspathl;
			else:
				if file == fname:
					foundabspathlist.append(abspname);
		return foundabspathlist;
		
	def reloaddeep(self,modname):
		pyfilename=modname+'.py';
		pycfilename=modname+'.pyc';
		try:
			os.remove(pycfilename);
		except:
			#print pycfilename, "not found."
			pass;
		plist=self.find(pyfilename);
		if len(plist)>0:
			for p in plist:
				self.reload(modname,p);
		return self['importstack'];
		
	def reload(self,modname,abspname):
		#print "import_:",modname;
		if self['importstack'].count(modname)==0:
			self['importstack'].append(modname);
			pyfilename=modname+'.py';
			fullfilename=os.path.join(abspname,pyfilename);
			fh=open(fullfilename);
			for line in fh:
				if line.startswith('from'):
					g=re.search("from (\S+) import *",line);
					if g is not None:
						premodname=g.group(1);
						#print "premodname:",premodname
						self.reloaddeep(premodname);
			fh.close();
			cmd='import '+modname;
			exec(cmd);
			cmd='reload('+modname+')';
			exec(cmd);
			XOS.importedmodnames.append(modname);
			#print modname,'reloaded'
			
	def reloadallxpymods(self):
		#print "Reloading all modules in:",self['rootpath'],' ...'
		self.reloadallmodindir(self['rootpath']);
		#print self['importedmodnames'];
		XOS.importedmodnames=set(XOS.importedmodnames);
		XOS.importedmodnames=list(XOS.importedmodnames);
		
	def reloadallmodindir(self,abspname):
		#print "reloading dir...",abspname
		files=os.listdir(abspname);
		for file in files:
			fullname=os.path.join(abspname, file);
			if os.path.isdir(fullname) and file[0]!='#':
				self.reloadallmodindir(fullname);
			else:
				li=os.path.split(fullname);
				pname=li[0];
				fname=li[1];
				li=fname.split(os.path.extsep);
				ext=li[-1];
				modname=li[0];
				if ext=='pyc' or ext=="py":
					self.reloaddeep(modname);
		#print "L stack ",len(self['importstack'])
		
	def fileparts(self,fullfilename):
		li=os.path.split(fullfilename);
		pname=li[0];
		fname=li[1];
		li=fname.split(os.path.extsep);
		fname=li[0];
		if len(li)>1:
			ext=li[-1];
		else:
			ext='';
		#print fullfilename
		#print (pname,fname,ext);
		return (pname,fname,ext);
		
	def filenameappend(self,fullfilename,str2append):
		#print "to append:",str2append
		pname,fname,ext=self.fileparts(fullfilename);
		fname=fname+'_'+str2append;
		fname=fname+os.path.extsep+ext;
		fname=os.path.join(pname,fname);
		return fname;


#=========================================
#=========================================
#functions
#=========================================
#=========================================
import pickle;
import gzip

def zippicksave(object, filename, protocol = 0):
	"""Saves a compressed object to disk
	"""
	file = gzip.GzipFile(filename, 'wb')
	file.write(pickle.dumps(object, protocol))
	file.close()

def zippickload(filename):
	"""Loads a compressed object from disk
	"""
	file = gzip.GzipFile(filename, 'rb')
	buffer = ""
	while 1:
		data = file.read()
		if data == "":
			break
		buffer += data
		object = pickle.loads(buffer)
		file.close()
	return object

def getcaller():
	import traceback;
	callers=traceback.extract_stack();
	return callers[-3];
#===========================================
#  file utility
#===========================================
def findinfile(filename,str2find):
	linenums=[];
	f=open(filename,"Ur");
	i=0;
	for line in f:
		i=i+1;
		found=line.find(str2find);
		if found!=-1:
			linenums.append(i);
	f.close();
	#print filename,linenums
	return linenums;

def findindir(pname,str2find):
	import os;
	found=[];
	files=os.listdir(pname);
	for file in files:
		fullname=os.path.join(pname,file);
		if os.path.isdir(fullname):
			#print fullname
			found1=findindir(fullname,str2find);
			found=found+found1;
		else:
			linenums=findinfile(fullname,str2find);
			if len(linenums)>0:
				record={};
				record['fname']=fullname;
				record['linenums']=linenums;
				found.append(record);
	return found;

	