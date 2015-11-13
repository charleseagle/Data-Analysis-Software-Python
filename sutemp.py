def ff(approot):
	a=approot['clipboard'];
	b=a['physsumrule0'];
	cm=[4035.5,8071.0,14527.8,24213.1];
	for f in cm:
		c=b.uipickcolumnvalue(f,'Temperature');
		c['x'].tofile('t.asc','\n');
		c['y'].tofile(str(f)+'.asc','\n');