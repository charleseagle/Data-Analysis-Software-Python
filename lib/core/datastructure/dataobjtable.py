from  dataobject import *;
import easygui;

class DataObjTable(DataObject):
	def __init__(self):
		self['_datobj_rownamelist']=[];
		pass;
		#self.set('dataobjlist',DataObject());

	def insert(self,dataobj,rowname=None):
		if rowname is None:
			keys=self.keys();
			rowname='row'+str(len(keys));
		self.set(rowname,dataobj);
		self['_datobj_rownamelist'].append(rowname);
		
	def select(self,columnlist,condition=True,selectNA=False,fuzzy=None):
		#objlist=;
		#dobjlist=self['dataobjlist'];
		#print dobjlist
		if columnlist=="*":
			columnlist=self.fullcolumnlist();
		datatable=self.getemptyinstance();
		for k in self.keys():
			row=self[k];
		#for i in range(0,len(dobjlist)):
			#print 'row:',i
		#	row=dobjlist[i]
			TF=self.testcondition(row,condition,selectNA,fuzzy=fuzzy);
			if TF:
				#rowobj=recoverdataobjclass(row);
				rowobj=row;
				rowobjnew=rowobj.getemptyinstance();
				#print type(row),type(rowobjnew)
				for ikey in columnlist:
					try:
						rowobjnew[ikey]=row[ikey];
					except:
						rowobjnew[ikey]=None;
				datatable.insert(rowobjnew,k);	
		return datatable
	
	def update(self,columnlist=None,newvaluelist=None,updatecmd=None,condition=False,selectNA=True):
		for k in self.keys():
			row=self[k];
		#for row in self['dataobjlist']:
			if self.testcondition(row,condition,selectNA):
				if updatecmd is not None:
					self.updaterowcmd(row,updatecmd);
				else:
					for i in range(len(columnlist)):
						row[columnlist[i]]=newvaluelist[i];
				
	def delete(self,condition=False,selectNA=False):
		for k in self.keys():
			row=self[k];
		#for row in self['dataobjlist']:
			if self.testcondition(row,condition,selectNA):
				del self[k];
				I=self['_datobj_rownamelist'].index(k);
				self['_datobj_rownamelist'].pop(I);
	
	
	def aggselect(self,_expression,_condition=True,_selectNA=False):
		for _column in self.fullcolumnlist():
			_cmd=_column+'=[]';
			#print _cmd;
			exec(_cmd);
		for _k in self.keys():
			_row=self[_k];
			if self.testcondition(_row,_condition,_selectNA):		
				for _column in self.fullcolumnlist():
					if _row.has_key(_column):
						#print '_row',_row, _row.has_key(_column)
						#print '_column',type(_column),_column
						#print 'found',_row[_column]
						_cmd=_column+'.append(_row[_column])';
						#print '_cmd:', _cmd
						exec(_cmd);
		#print "rowname:",self.keys()
		#print "columnname",self.fullcolumnlist();
		#print "xlen:",len(x)
		return eval(_expression);
	
	def indopselect(self,_expression,_cmd,_condition=True,_selectNA=False):
		resultdict=dict();
		for rowname in self.keys():
			_row=self[rowname];
			if self.testcondition(_row,_condition,_selectNA):
				for _column in self.fullcolumnlist():
					if _row.has_key(_column):
						_cmd0=_column+"=_row['"+_column+"']";
						#print _cmd0
						exec(_cmd0);
				exec(_cmd);
				result=eval(_expression);
				resultdict[rowname]=result;
				#_rowobj=recoverdataobjclass(_row);
				#resultrow=_rowobj.getemptyinstance();
				#resultrow.set('selected',result);
				#resulttable.insert(resultrow,rowname);
		return resultdict;
	
	def groupsingle(self,_expression,_condition=True,_selectNA=False,_fuzzy=None):
		_cmd='_result='+_expression;
		_resultdict=self.indopselect('_result',_cmd,_condition,_selectNA);
		_resultlist=list(set(_resultdict.values()));
		if _fuzzy is not None:
			_resultlist=self.fuzzyset(_resultlist,_fuzzy);
		_resultlist.sort();
		#print "_resultlist",_resultlist
		tablegroups=[];
		for _result in _resultlist:
			subgroup=self.select("*",_condition,_selectNA);
			_cond=[_expression,_result]
			#print "_condr",_cond
			subgroup=subgroup.select("*",_cond,_selectNA,_fuzzy);
			#print len(subgroup.keys())
			tablegroups.append(subgroup);
		return 	tablegroups;
		
	def group(self,_explist,_condition=True,_selectNA=False,_fuzzy=None):
		print "group:",_explist
		if not isinstance(_explist,list):
			_explist=[_explist];
			#_explist=eval('['+_explist+']');
			#_explist=_explist.split();
			#print "_explist",_explist
			
		_exp=_explist[0];
		tablegroups=self.groupsingle(_exp,_condition,_selectNA,_fuzzy);
		for _exp in _explist[1:]:
			tablegroups0=[];
			for g in tablegroups:
				g1=g.groupsingle(_exp,_condition,_selectNA);
				tablegroups0=tablegroups0+g1;
				#print "g1 len",len(g1)
			tablegroups=tablegroups0;
		return tablegroups;
	
	def keyssorted(self,_explist,_condition=True,_selectNA=False):
		groups=self.group(_explist,_condition=True,_selectNA=False);
		keylist=[];
		for g in groups:
			keylist=keylist+g.keys();
		return keylist;
		
	
#|########################################################
#|#####################################################3333
	
	def deletecol(self,columnlist=None,condition=False,selectNA=False):
		for k in self.keys():
			row=self[k];
		#for row in self['dataobjlist']:
			if self.testcondition(row,condition,selectNA):
				for column in columnlist:
					try:
						del row[column];
					except:
						a=1;
						
	def updaterowcmd(self,_row,_updatecmd):
		_oldkeys=_row.keys();
		for _iupdaterow in _row.keys():
			_cmd=_iupdaterow+"=_row['"+_iupdaterow+"']";
			exec(_cmd);
		exec(_updatecmd);
		#print "updatecmd:",_updatecmd
		#print "Temperature:",Temperature
		for _iupdaterow in _oldkeys:
			_cmd="_row['"+_iupdaterow+"']="+_iupdaterow;
			exec(_cmd);
		
	def fixNA4col(self,_columnlist=None):
		for k in self.keys():
			_row=self[k];
		#for _row in self['dataobjlist']:
			for _column in _columnlist:
				if not _row.has_key(_column):
					_row[_column]='';
				
	def testcondition(self,row,condition,selectNA,fuzzy=None):
		#print condition
		TF=False;
		#print "in testcondition:",condition
		for j in row.keys():
			#print 'proname:',j
			cmd=j+"=row['"+j+"']";
			#print 'cmd:',cmd;
			exec(cmd)
		if isinstance(condition,list):
			TF=row.datopcompare(condition[0],condition[1],fuzzy);
		else:	
			TF=condition;
		if not (TF==True or TF==False):
			try:
				TF=eval(condition);
				#print "TF expression",TF
			except:	
				TF=selectNA;
				#print "TF NA",TF
		#print TF	
		"""if isnumeric(TF):
			print 'Error: expect logic condition, got numeric'
			TF=False;
		"""	
		return TF;
		
	def fullcolumnlist(self):
		columnlist=[];
		for k in self.keys():
			row = self[k];
		#for row in self['dataobjlist']:
			for colk in row.keys():
				#print "rowk",k,"colk",colk
				columnlist.append(colk);
		columnlist=set(columnlist);	
		columnlist=list(columnlist);
		return columnlist;
		
	def nrow(self):
		return len(self.keys());
		
	def merge(self,table2):
		for k in table2.keys():
			row=table2.get(k);
			self.insert(row,k);
			
	def seqkeys(self):
		return self['_datobj_rownamelist'];
	
	def dispseqkeys(self):
		print self['_datobj_rownamelist'];
	
	"""
	def contextmenu(self,menu,dataname=''):
		import time,os;
		menu=DataObject.__dict__['contextmenu'](self,menu,dataname);
		#menu=DataObject.contextmenu(self,menu);
		menu.add_separator();
		menu.add_command(label="Data command",command=lambda:self.sqlcmd(menu));
		return menu;
	"""
	def uidatacommand(self,menu):
		samplecmds='Examples:\n';
		samplecmds=samplecmds+"print self.keys()\n";
		samplecmds=samplecmds+"self.update(columnlist=['x','y'],newvaluelist=[1,2],condition=True)\n";
		samplecmds=samplecmds+"self.update(updatecmd='x=1',condition=True)\n";
		samplecmds=samplecmds+"self.update(updatecmd=\"_row['xunit'].setcurrentunit('eV')\",condition=True)\n";
		answer=easygui.enterbox(samplecmds,"SQL command","print self.keys()");
		if answer is not None:
			cmd=answer;
			exec(cmd);
			menu.stdout(answer);
			
	def fuzzyset(self,li,tolerance):
		import copy;
		li0=copy.copy(li);
		ll=[];
		while len(li0)>0:
			li1=copy.copy(li0);
			l0=[];
			for k in li1:
				#k=li1[i];
				toadd=False;
				if len(l0)==0:
					toadd=True;
				elif abs(mean(l0)-k)<tolerance:
					toadd=True;
				if toadd:
					l0.append(k);
					li0.pop(li0.index(k));
			ll.append(l0);
		for i in range(len(ll)):
			ll[i]=mean(ll[i]);
		#print ll.sort();
		return ll;
		
		
		
		