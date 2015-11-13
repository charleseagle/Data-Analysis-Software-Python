from filewin import *;
from dataobjtable import*;
from emwspectrum import *;
from plotabledataobjtable import *;
from Tkinter import *;
from datamenu import *;
import os;

class EMWSpectExp(FileWin):
	def __init__(self,parentdatawin=None,winname='unnamed'):
		FileWin.__dict__['__init__'](self,parentdatawin,winname);
		self.__ginit();
		self.setsavabledata('rawspectra',PlotableDataObjTable());
		#self['dataexplorerframeclass']={'modulename':'dataexplorerplotframe','typename':'DataExplorerPlotFrame'};
		self.uiexploredata();
		
	def __ginit(self):
		self.setting(False);
		
		self.addmenu(None,"Rawdata","Default setting",self.setting);
		self.addmenu(None,"Rawdata","Import WinLab(Ratio)",lambda: self.importrawdata("winlab"));
		self.addmenu(None,"Rawdata","Import WinLabSingleBasis",lambda: self.importrawdata("winlabsinglebase"));
		self.addmenu(None,"Rawdata","Import WinLabSingleBasis Dir",lambda: self.importrawdata("winlabsinglebasedir"));
		self.addmenu(None,"Rawdata","Import WinLabDoubleBasis",lambda: self.importrawdata("winlabdoublebase"));
		self.addmenu(None,"Rawdata","Import OPUS(Referen&Sample)",lambda: self.importrawdata("opus"));
		self.addmenu(None,"Rawdata","Import NHMFL(batch)",lambda: self.importrawdata("nhmfl"));
		self.addmenu(None,"Rawdata","Import dir",lambda: self.importrawdata("dir"));
		
		b=self.addbutton(lambda: self.importrawdata("winlab"),text=None,imagefname="face-monkey_003.png");
		self['balloon'].bind(b,"Import single spectrum");
		
		anamenu=self.menu('Analysis');

		resizemenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Resize",menu=resizemenu);
		resizemenu.add_command(label="Pick spectra part",command=lambda: self.addextcontrol("Fr_SpectraRangePick","fr_spectrarangepick"));
		resizemenu.add_command(label="Extend Spectra",command=lambda: self.addextcontrol("Fr_SpectExtend","fr_spectextend"));
		resizemenu.add_command(label="Cull Spectra",command=lambda: self.addextcontrol("Fr_SpectCull"));
		resizemenu.add_command(label="Refine Spectra",command=lambda: self.addextcontrol("Fr_SpectRefine"));
		
		# calculation
		calmenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Database",menu=calmenu);
		calmenu.add_command(label="Binary Calculation",command=lambda: self.addextcontrol("Fr_SpectCalBinary"));
		calmenu.add_command(label="Auto Binary Calculation",command=lambda: self.addextcontrol("Fr_SpectCalBinaryAuto"));
		calmenu.add_command(label="Update by command",command=lambda: self.addextcontrol("Fr_SpectSetColValue"));
		calmenu.add_command(label="Aggregation",command=lambda: self.addextcontrol("Fr_SpectCalAggregation"));
		calmenu.add_command(label="Spect Aggregation",command=lambda: self.addextcontrol("Fr_SpectCalSpectAggregation"));
		calmenu.add_command(label="Cumulative Sum",command=lambda: self.addextcontrol("Fr_SpectCumSum"));
		#calmenu.add_command(label="Ratio",command=lambda: self.addextcontrol("Fr_SpectraRatio","fr_spectraratio"));
		#calmenu.add_command(label="Difference",command=lambda: self.addextcontrol("Fr_SpectraDiff","fr_spectradiff"));
		#calmenu.add_command(label="RS ratio",command=lambda: self.addextcontrol("Fr_SpectraRSRatio","fr_spectrarsratio"));
		
		# for peak analysis
		peakmenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Peak analysis",menu=peakmenu);
		peakmenu.add_command(label="Moments",command=lambda: self.addextcontrol("Fr_PeakInfo"));
		peakmenu.add_command(label="Gaussian",command=lambda: self.addextcontrol("Fr_PeakInfoGauss"));
		peakmenu.add_command(label="Exp Decay Fit",command=lambda: self.addextcontrol("Fr_PeakInfoExpDecay"));
		peakmenu.add_command(label="Gaussian Deconvolution",command=lambda: self.addextcontrol("Fr_GaussDeconv"));
		
		# for renormalization
		renmenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Renormalize",menu=renmenu);
		renmenu.add_command(label="Internal",command=lambda: self.addextcontrol("Fr_SpectInternalRenorm","fr_spectinternalrenorm"));
		renmenu.add_command(label="External",command=lambda: self.addextcontrol("Fr_SpectExternalRenorm","fr_spectexternalrenorm"));
		renmenu.add_command(label="Manual",command=lambda: self.addextcontrol("Fr_SpectManualRenorm","fr_spectmanualrenorm"));
		renmenu.add_command(label="Reshape",command=lambda: self.addextcontrol("Fr_SpectReshapeRenorm","fr_spectreshaperenorm"));
		renmenu.add_command(label="Reference correction",command=lambda: self.addextcontrol("Fr_SpectRefRenorm","fr_spectrefrenorm"));
		renmenu.add_command(label="Custom",command=lambda: self.addextcontrol("Fr_SpectCustomRenorm"));
		
		# for merging
		mergemenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Merge",menu=mergemenu);
		#mergemenu.add_command(label="Mean",command=lambda: self.addextcontrol("Fr_SpectMeanMerge","fr_spectmeanmerge"));
		mergemenu.add_command(label="Auto",command=lambda: self.addextcontrol("Fr_SpectAutoMerge"));
		mergemenu.add_command(label="Individual",command=lambda: self.addextcontrol("Fr_SpectIndMerge","fr_spectindmerge"));
		
		# for other tools
		othermenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Tools",menu=othermenu);
		othermenu.add_command(label="Smooth",command=lambda: self.addextcontrol("Fr_SpectSmooth","fr_spectsmooth"));
		othermenu.add_command(label="Fix glich",command=lambda: self.addextcontrol("Fr_SpectFixGlich","fr_spectfixglich"));
		othermenu.add_command(label="Fix jump",command=lambda: self.addextcontrol("Fr_SpectFixJump"));
		othermenu.add_command(label="Fix notch",command=lambda: self.addextcontrol("Fr_SpectFixNotch"));
		othermenu.add_command(label="Contrain y",command=lambda: self.addextcontrol("Fr_SpectYConstrain"));
		othermenu.add_command(label="Adjust x",command=lambda: self.addextcontrol("Fr_SpectXAdjust"));
		
		# for reference change approach
		refchangemenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Reference change approach",menu=refchangemenu);
		refchangemenu.add_command(label="Find reference change",command=lambda: self.addextcontrol("Fr_SpectFindRefChange"));
		refchangemenu.add_command(label="Apply reference change",command=lambda: self.addextcontrol("Fr_SpectApplyRefChange"));
		refchangemenu.add_command(label="Film correction",command=lambda: self.addextcontrol("Fr_SpectFilmCorrection"));
		
		
		#refchangemenu.add_command(label="Calculate ratio",command=lambda: self.addextcontrol("Fr_SpectCalRatio"));

		# for physical calculation
		physmenu=DataMenu(anamenu,tearoff=0);
		anamenu.add_cascade(label="Physical",menu=physmenu);
		physmenu.add_command(label="From transmittance to absorption coefficient",command=lambda: self.addextcontrol("Fr_SpectAbsorption"));
		physmenu.add_command(label="Phase shift",command=lambda: self.addextcontrol("Fr_SpectPhaseShift","fr_spectphaseshift"));
		physmenu.add_command(label="Optical functions",command=lambda: self.addextcontrol("Fr_SpectOptConst","fr_spectoptconst"));
		physmenu.add_command(label="Direct gap",command=lambda: self.addextcontrol("Fr_SpectDirectGap"));
		physmenu.add_command(label="Indirect gap",command=lambda: self.addextcontrol("Fr_SpectIndirectGap"));
		physmenu.add_command(label="Sum rule",command=lambda: self.addextcontrol("Fr_SpectSumRule"));
		physmenu.add_command(label="Calculate n,k from R and T",command=lambda: self.addextcontrol("Fr_SpectRT2nk"));
		physmenu.add_command(label="Calculate n,k from R and T Film",command=lambda: self.addextcontrol("Fr_SpectFilmRT2nk"));
		physmenu.add_command(label="Pellet Fit",command=lambda: self.addextcontrol("Fr_SpectPelletFit"));
		physmenu.add_command(label="Absorption 2 color",command=lambda: self.addextcontrol("Fr_ColorSpect"));
		
	def setting(self,gui=True):
		defaultsetting=self.getsavabledata('defaultsetting');
		if defaultsetting is None:
			#print self['savabledata'].keys()
			defaultsetting=DataObject();
			defaultsetting['Temperature']=300;
			defaultsetting['Mag_Field']=0;
			defaultsetting['Polarization']=0;
		else:
			#print 'found old setting'
			#print self['savabledata']['defaultsetting'];
			defaultsetting=self.getsavabledata('defaultsetting');
		
		if gui==True:
			defaultsetting.uiset(datatype="numeric");
		#print defaultsetting;
		self.setsavabledata('defaultsetting',defaultsetting);
		#print self['savabledata']['defaultsetting'];
		#print self['savabledata'].keys()
	
	def importrawdata(self,filekind):
		success=False;
		#here we need to take care of the path etc.
		rawspect=self.getsavabledata('rawspectra');
		if rawspect is None:
			self.setsavabledata('rawspectra',PlotableDataObjTable());
		import easygui,os;
		pathstr=self.getasciipath();
		if pathstr is not None:
			initialfile=os.path.join(pathstr,"*.*");
		else:
			initialfile="*.*";
		fullfilechosen=easygui.fileopenbox('Please choose a file (Ref for opus) to open','Opeing a file...',initialfile);
		if fullfilechosen is not None:
			li=os.path.split(fullfilechosen);
			pathstr=li[0];
			filename=li[1];
			if filekind=="winlab":
				success=self.importwinlab(pathstr,filename);
			elif filekind=="winlabsinglebase":
				success=self.importwinlabsinglebase(pathstr,filename);
			elif filekind=="winlabsinglebasedir":
				success=self.importwinlabsinglebasedir(pathstr,filename);
			elif filekind=="winlabdoublebase":
				success=self.importwinlabdoublebase(pathstr,filename);
			elif filekind=="opus":
				success=self.importopus(pathstr,filename);
			elif filekind=="nhmfl":
				success=self.importnhmfl(pathstr,filename);
			elif filekind=="dir":
				success=self.importdir(pathstr,filename);
			if success:
				self.setasciipath(pathstr);
				import pylab;
				rawspectra=self.getsavabledata('rawspectra');
				rawspectra.plot();
				#pylab.show();
		else:
			self.stdout( "import rawdata canceled");
			
	def importwinlab(self,pathstr,filename):
		spect=self.importwinlab_nonui(pathstr,filename);
		spect.uiset(datatype='string');
		spect.uiset(datatype='numeric');
		spect.convertx('cm_1');
		
		rawspect=self.getsavabledata('rawspectra');
		#print type(rawspect)
		rawspect.insert(spect,filename);
		self.setsavabledata('rawspectra',rawspect);
		return True;	
			
	def importwinlab_nonui(self,pathstr,filename):
		import os;
		fullfilechosen=os.path.join(pathstr,filename);
		#print "filechosen",fullfilechosen
		spect=EMWSpectrum(fullfilechosen,"\t");
		spect.import_();
		
		# get information from header
		xunit=spect.getfromheader("#GR","tokenline")
		if isinstance(xunit,str):
			xunitobj=spect.get('xunit');
		#print "xunitobj",xunitobj
			xunitobj.setcurrentunit(xunit.lower());
			spect.set('xunit',xunitobj);
		spect['xunit'].uisetcurrentunit();
		
		yname=spect.getfromheader(76,"lineNo");
		#print "yname:",yname
		yunitobj=spect.get('yunit');
		yunitobj.setcurrentunit(varname=yname);
		#yunitobj.uisetcurrentunit();
		spect.set('yunit',yunitobj);
		
		dsetting=self.getsavabledata('defaultsetting');
		spect['Temperature']=dsetting['Temperature'];
		spect['Mag_Field']=dsetting['Mag_Field'];
		spect['Polarization']=dsetting['Polarization'];
		
		self.stdout(("Winlab file",filename,"imported",spect['num_matrix'].shape));
		
		return spect;
	
	def import_nonui(self,pathstr,filename):
		import os;
		fullfilechosen=os.path.join(pathstr,filename);
		#print "filechosen",fullfilechosen
		spect=EMWSpectrum(fullfilechosen,"\t");
		spect.import_();

		xunit="cm_1"
		if isinstance(xunit,str):
			xunitobj=spect.get('xunit');
			xunitobj.setcurrentunit(xunit.lower());
			spect.set('xunit',xunitobj);
		#spect['xunit'].uisetcurrentunit();
		
		#yname=spect.getfromheader(76,"lineNo");
		yname="yname"
		#print "yname:",yname
		#yunitobj=spect.get('yunit');
		#yunitobj.setcurrentunit(varname=yname);
		#yunitobj.uisetcurrentunit();
		#spect.set('yunit',yunitobj);
		
		dsetting=self.getsavabledata('defaultsetting');
		spect['Temperature']=dsetting['Temperature'];
		spect['Mag_Field']=dsetting['Mag_Field'];
		spect['Polarization']=dsetting['Polarization'];
		
		self.stdout(("Winlab file",filename,"imported",spect['num_matrix'].shape));
		
		return spect;
		
	def importwinlabdoublebase(self,pathstr,filename):
		success=False;
		import easygui,numpy;
		inputfieldValue =easygui.enterbox("Temperature list?", "WinLabDoubleBase", '[300,400]');
		if inputfieldValue is not None:
			temp_range=list(eval(inputfieldValue));
			for T in temp_range:
				if len(filename)==12:
					fname=filename.replace(filename[5:8],str(T));	
				elif len(filename)==11:
					fname=filename.replace(filename[5:7],str(T));	
				
				fname_m1=fname.replace(fname[-2:],'m1');
				fname_m0=fname.replace(fname[-2:],'m0');
				fname_s1=fname.replace(fname[-2:],'s1');
				fname_s0=fname.replace(fname[-2:],'s0');
				
				spect_m1=self.importwinlab_nonui(pathstr,fname_m1);
				spect_m1['Temperature']=T;
				
				if temp_range.index(T)==0:
					spect=spect_m1;
					spect.numstrsetting();
					xunitobj=spect.get('xunit');
					xunitobj.uiset('string');
					spect.set('xunit',xunitobj);
					spect0=spect.copy();
				else:
					spect0.copynumstrsettingto(spect_m1);
				
				#print "spect0 xunit",spect0['xunit'] 
				
				spect_m1['xunit']=spect0['xunit'].copy();
				spect_m1.convertx('cm_1');			
				#print "spect0 xunit",spect0['xunit'] 
				
				spect_m0=self.importwinlab_nonui(pathstr,fname_m0);
				spect0.copynumstrsettingto(spect_m0);
				spect_m0.set('xunit',spect0.get('xunit').copy());
				spect_m0.convertx('cm_1');			

				spect_s1=self.importwinlab_nonui(pathstr,fname_s1);
				spect0.copynumstrsettingto(spect_s1);
				spect_s1.set('xunit',spect0.get('xunit').copy());
				#spect_s1['xunit']=spect0['xunit'].copy();
				spect_s1.convertx('cm_1');			
				
				spect_s0=self.importwinlab_nonui(pathstr,fname_s0);
				spect0.copynumstrsettingto(spect_s0);
				spect_s0.set('xunit',spect0.get('xunit').copy());
				#spect_s0['xunit']=spect0['xunit'].copy();
				spect_s0.convertx('cm_1');			
				
				
				x=spect_m1['x'];
				ym1=spect_m1['y'];
				ym0=spect_m0['y'];
				ys1=spect_s1['y'];
				ys0=spect_s0['y'];
				y=(ys1-ys0)/(ym1-ym0);
				
				data=numpy.vstack((x,y,ym1,ym0,ys1,ys0));
				spect=spect_m1;
				spect['num_matrix']=numpy.transpose(data);
				spect.setupxy();
				spect['Temperature']=T;
				
				rawspect=self.getsavabledata('rawspectra');
				rawspect.insert(spect,str2varname(fname[0:-2]));
				self.setsavabledata('rawspectra',rawspect);	
				
				#raw_input('pause for import raw data');
			success=True;
		return success;	
	
	def importwinlabsinglebase(self,pathstr,filename):
		success=False;
		import easygui,numpy;
		inputfieldValue =easygui.enterbox("Temperature list?", "WinLabSingleBase", '[300,400]');
		if inputfieldValue is not None:
			temp_range=list(eval(inputfieldValue));
			
			self.getrootdatawin().stdout(temp_range);
			
			for T in temp_range:
				self.getrootdatawin().stdout(("T:",T));
				if len(filename)==12:
					self.stdout("filename12");
					fname=filename.replace(filename[5:8],str(T));	
				elif len(filename)==11:
					self.stdout("filename11");
					fname=filename.replace(filename[5:7],str(T));	
				self.stdout(("fname:",fname));
				fname_m1=fname[0:-1]+'1';
				fname_m0=fname[0:-1]+'0';
				
				spect_m1=self.importwinlab_nonui(pathstr,fname_m1);
				spect_m1['Temperature']=T;
				
				if temp_range.index(T)==0:
					spect=spect_m1;
					spect.numstrsetting();
					xunitobj=spect.get('xunit');
					xunitobj.uiset('string');
					spect.set('xunit',xunitobj);
					spect0=spect.copy();
				else:
					spect0.copynumstrsettingto(spect_m1);
				
				#print "spect0 xunit",spect0['xunit'] 
				
				spect_m1['xunit']=spect0['xunit'].copy();
				spect_m1.convertx('cm_1');			
				#print "spect0 xunit",spect0['xunit'] 
				
				spect_m0=self.importwinlab_nonui(pathstr,fname_m0);
				spect0.copynumstrsettingto(spect_m0);
				spect_m0.set('xunit',spect0.get('xunit').copy());
				spect_m0.convertx('cm_1');						
				
				x=spect_m1['x'];
				ym1=spect_m1['y'];
				ym0=spect_m0['y'];
				y=(ym1-ym0);
				
				data=numpy.vstack((x,y,ym1,ym0));
				spect=spect_m1;
				spect['num_matrix']=numpy.transpose(data);
				spect.setupxy();
				spect['Temperature']=T;
				
				rawspect=self.getsavabledata('rawspectra');
				rawspect.insert(spect,str2varname(fname[0:-1]));
				self.setsavabledata('rawspectra',rawspect);	
				
				#raw_input('pause for import raw data');
			success=True;
		return success;

	def importwinlabsinglebasedir(self,pathstr,filename):
		success=False;
		import easygui,numpy;
		inputfieldValue =easygui.enterbox("Expname?", "ImportWinlabSingleDir", filename[0:-7]);
		if inputfieldValue is not None:
			expname=inputfieldValue;
			files=os.listdir(pathstr);
			firstspect=True;
			for file in files:
				fullname=os.path.join(pathstr, file);
				#print file,'ext:',ext
				if not os.path.isdir(fullname) and file.startswith(expname):
					li=file.split(os.path.extsep);
					prefix=li[0];
					#self.stdout(prefix);
					Tstr=prefix.replace(expname,"");
					ext=li[-1];
					#self.stdout(Tstr);
					#self.stdout(ext);
					T=None;
					try:
						T=int(Tstr);
						self.stdout(T);
					except:
						T=None;
					if T is not None:
						fname_m1=file[0:-1]+'1';
						fname_m0=file[0:-1]+'0';
						try:
							spect_m1=self.importwinlab_nonui(pathstr,fname_m1);
							spect_m1['Temperature']=T;
				
							if firstspect:
								spect=spect_m1;
								spect.numstrsetting();
								xunitobj=spect.get('xunit');
								xunitobj.uiset('string');
								spect.set('xunit',xunitobj);
								spect0=spect.copy();
								firstspect=False;
							else:
								spect0.copynumstrsettingto(spect_m1);
				
							spect_m1['xunit']=spect0['xunit'].copy();
							spect_m1.convertx('cm_1');
							spect_m0=self.importwinlab_nonui(pathstr,fname_m0);
							spect0.copynumstrsettingto(spect_m0);
							spect_m0.set('xunit',spect0.get('xunit').copy());
							spect_m0.convertx('cm_1');
				
							x=spect_m1['x'];
							ym1=spect_m1['y'];
							ym0=spect_m0['y'];
							y=(ym1-ym0);
				
							data=numpy.vstack((x,y,ym1,ym0));
							spect=spect_m1;
							spect['num_matrix']=numpy.transpose(data);
							spect.setupxy();
							spect['Temperature']=T;
				
							rawspect=self.getsavabledata('rawspectra');
							rawspect.insert(spect,str2varname(file[0:-1]));
						except:
							pass;
				#raw_input('pause for import raw data');
			success=True;
		return success;
		
	def importdir(self,pathstr,filename):
		success=False;
		firstspect=True;
		import easygui,numpy;
		files=os.listdir(pathstr);
		for file in files:
			setting0=self.getsetting_fromfilename(file);
			fullname=os.path.join(pathstr, file);
			print "file:",file
			#print file,'ext:',ext
			if not os.path.isdir(fullname):
				try:
					spect_m1=self.import_nonui(pathstr,file);
					if firstspect:
						#print "first spect"
						spect=spect_m1;
						spect.numstrsetting();
						xunitobj=spect.get('xunit');
						xunitobj.uiset('string');
						spect.set('xunit',xunitobj);
						spect0=spect.copy();
						firstspect=False;
					else:
						spect0.copynumstrsettingto(spect_m1);
						spect_m1['xunit']=spect0['xunit'].copy();
						spect_m1.convertx('cm_1');
						spect=spect_m1;

					if setting0['Temperature'] is not None:
						spect['Temperature']=setting0['Temperature'];
					rawspect=self.getsavabledata('rawspectra');
					rawspect.insert(spect,str2varname(file[0:-1]));
				except:
					print"import_noui error:",file
					pass;
				#raw_input('pause for import raw data');
			success=True;
		return success;
		
	def importopus(self,pathstr,reffilename):
		success=0;
		initialfile=os.path.join(pathstr,"*.*");
		fullreffilechosen=os.path.join(pathstr,reffilename);
		fullsplfilechosen=easygui.fileopenbox('Please choose a sample file to open','Opeing a file...',initialfile);
		if fullsplfilechosen is not None:
			refspect=EMWSpectrum(fullreffilechosen,"\t");
			refspect.import_();
			#print "Lx:",len(refspect['x']),min(refspect['x']);
			splspect=EMWSpectrum(fullsplfilechosen,"\t");
			splspect.import_();
			#print "Lx:",len(splspect['x']),min(splspect['x']);
			refspect.get('xunit').uiset("string");
			refspect.copynumstrsettingto(splspect);
			#refspect.numstrsetting();
			splspect.numstrsetting();
			splspect.binop(refspect,"/");
			self['savabledata']['rawspectra'].insert(splspect,reffilename);
			success=1;
		return success;

	def importnhmfl(self,pathstr,filename):
		success=0;
		#fullreffilechosen=os.path.join(pathstr,reffilename);
		answer=easygui.enterbox("Expname length","Loading NHMFL files","3");
		if answer is not None:
			lexpname=int(answer);
			expname=filename[0:lexpname];
			files=os.listdir(pathstr);
			i=0;
			for file in files:
				if not os.path.isdir(file):
					if file[0:lexpname]==expname:
						if i==0:
							spect=self.importnhmfl_nonui(pathstr,file);
							xunitobj=spect.get('xunit');
							xunitobj.uiset('string');
							#spect.set('xunit',xunitobj);
							spect0=spect.copyxy();
							i=i+1;
						else:
							spect=self.importnhmfl_nonui(pathstr,file,spect0);
						spect.convertx("cm_1");
						self['savabledata']['rawspectra'].insert(spect,file);
			success=1;
		return success;
		
	def importnhmfl_nonui(self,pathstr,file,spect0=None):
		self.stdout(file);
		fullfilechosen=os.path.join(pathstr,file);
		spect=EMWSpectrum(fullfilechosen,"\t");
		spect.import_();
		T=spect.getfromheader("(\S+)(\s+)Temperature(\s+)(\S+)(\s+)([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)","pattern",7);
		B=spect.getfromheader("(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?), @ Magnet ID:","pattern",9);
		if spect0 is not None:
			spect0.copynumstrsettingto(spect);
			spect['xunit']=spect0['xunit'].copy();
		spect['Temperature']=float(T);
		spect['Mag_Field']=float(B);
		self.stdout(('T:',T,"B:",B));
		#spect.convertx('cm_1');
		#print "convertx"
		return spect;
		
	def getsetting_fromfilename(self,fname):
		Tstr=None;
		import re;
		setting0=DataObject();
		condition="(\S+)_(\S+)K(\S+)"
		g=re.search(condition,fname);
		try:
			Tstr=g.groups()[1];
		except:
			pass;
		if Tstr is not None:
			setting0['Temperature']=float(Tstr);
		else:
			setting0['Temperature']=None;
		return setting0;