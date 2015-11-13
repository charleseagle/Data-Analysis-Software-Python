from dataobject import *;
import csv;

class NumMatrixCSV(DataObject):
	def __init__(self,filename=None,dilimiter="\t",row_width_chosen="max"):
		self['filename']=filename;
		self['dilimiter']=dilimiter;
		self['row_width_chosen']=row_width_chosen;
		self['num_matrix']=None;
		#if filename!=None:
		#	self.importcsv();
			
	def importcsv(self,filename=None):
		if filename is not None:
			self['filename']=filename;
		reader = csv.reader(open(self['filename'], "rb"),delimiter=self['dilimiter']);
		numeric_rows=[];
		numeric_rows_width=[];
		for row in reader:
			try:
				valid_num_row=[];
				for element in row:
					f=float(element);
					valid_num_row.append(f);
			except:
				valid_num_row=self.analyzerow(row[0],None);
				if len(valid_num_row)==0:
					valid_num_row=self.analyzerow(row[0],'\t');
				if len(valid_num_row)==0:
					valid_num_row=self.analyzerow(row[0],',');
					
			if 	len(valid_num_row)>0:
				numeric_rows.append(valid_num_row);
				numeric_rows_width.append(len(valid_num_row));
		
		row_width_kind=list(set(numeric_rows_width));
		#print "row_width_kind",row_width_kind
		row_width_chosen=self['row_width_chosen'];
		try:
			index=row_width_kind.index(row_width_chosen);
			self['row_width_chosen']=row_width_kind[index];
		except:
			if row_width_chosen=="max":
				self['row_width_chosen']=max(row_width_kind);
			elif row_width_chosen=="min":
				self['row_width_chosen']=min(row_width_kind);
		#print "row_width_chosen",self['row_width_chosen']
		
		num_matrix_list=self.getnummatrix(numeric_rows,self['row_width_chosen']);
		#NrowNcol=self.findNcolNrow(NumCols);
		#dptablelist=self.formdptable(numeric_rows,self['row_width_chosen']);
		import numpy;
		num_matrix_array=numpy.array(num_matrix_list);
		self['num_matrix']=num_matrix_array;
		#print self['filename'],'imported.'
		#print 'Found arrary with shape:',num_matrix_array.shape;
			
	def getfromheader(self,condition,method="pattern"):
		resultstr=None;
		f=open(self['filename']);
		flist=list(f);
		f.close();	
		#print "len(f)",len(flist)
		#print "method:",method
		if method=="pattern":
			import re;
			for line in flist:
				g=re.search(condition,line);
				try: 	
					resultstr=g.group(1);
					break;
				except:
					pass;
		elif method=="lineNo":
			resultstr=flist[condition];
		elif method=="tokenline":
			import string;
			foundtoken=False;
			for line in flist:
				#print line,condition
				if foundtoken:
					resultstr=line;
					break;
				if string.strip(line)==condition:
					foundtoken=True;
					#print "foundtoken"
		else:
			print "wrong method:",method
		if isinstance(resultstr,str):
			resultstr=resultstr.replace("\n",'');
		return resultstr;
	
	def findNcolNrow(self,NumCols):
		NumColskind=list(set(NumCols));
		Nrows=[];
		for NCol in NumColskind:
			Nrows.append(NumCols.count(NCol));
		Nrowmax=max(Nrows);
		#print Nrows,Nrowmax
		#print type(Nrows),type(Nrowmax),
		index=Nrows.index(Nrowmax);
		Ncol=NumColskind[index];	
		#print "Nrow:",Nrowmax,"Ncol:",Ncol
		NN=[Nrowmax,Ncol];
		return NN;
		
	def getnummatrix(self,Numline,Ncol):
		import numpy;
		dptable=[];
		#print numpy.shape(Numline);
		for row in Numline:
			#print "row:",row,type(row);
			if len(row)==Ncol:
				dptable.append(row);
		return dptable;		
	
	def analyzerow(self,row,sep):
		ele0=row;
		#ele0=row[0];
		row0=ele0.split(sep);
		#print "ele0",ele0,"row0",row0;
		try:
			valid_num_row=[];
			for element in row0:
				f=float(element);
				valid_num_row.append(f);
			#print valid_num_row
		except:
			valid_num_row=[];
		return valid_num_row;