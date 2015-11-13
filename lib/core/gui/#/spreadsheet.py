import Tkinter as tk

root = tk.Tk()
root.title('Tkinter spreadsheet phase 1')

def click(event, cell):
# can do different things with right (3) and left (1) mouse button clicks
	root.title("you clicked mouse button %d in cell %s" % (event.num, cell))
# test right mouse button for equation solving
# eg. data = '=9-3' would give 6
	if event.num == 3:
# entry object in use
		obj = dict[cell]
# get data in obj
		data = obj.get()
# if it starts with '=' it's an equation
	if data.startswith('='):
		eq = data.lstrip('=')
		print data, eq
		try:
# solve the equation
			result = eval(eq)
#print result, type(result) # test
# remove equation data
			obj.delete(0, 'end')
# update cell with equation result
			obj.insert(0, str(result))
		except:
			pass

def key_r(event, cell):
# return/enter has been pressed
	data = dict[cell].get() # get text/data in given cell
#print cell, dict[cell], data # test
	root.title("cell %s contains %s" % (cell, data))

# create a dictionary of key:value pairs
dict = {}
w = 20
h = 1
alpha = ["", 'A', 'B', 'C', 'D', 'E', 'F']
for row in range(5):
	for col in range(5):
		if col == 0:
# create row labels
			label1 = tk.Label(root, width=3, text=str(row))
			label1.grid(row=row, column=col, padx = 2, pady=2)
		elif row == 0:
# create column labels
			label1 = tk.Label(root, width=w, text=alpha[col])
			label1.grid(row=row, column=col, padx = 2, pady=2) 
		else:
# create entry object
			entry1 = tk.Entry(root, width=w)
# place the object
			entry1.grid(row=row, column=col) #, padx = 2, pady=2)
# create a dictionary of cell:object pair
			cell = "%s%s" % (alpha[col], row)
			dict[cell] = entry1
# bind the object to a left mouse click
			entry1.bind('<Button-1>', lambda e, cell=cell: click(e, cell))
# bind the object to a right mouse click
			entry1.bind('<Button-3>', lambda e, cell=cell: click(e, cell))
# bind the object to a return/enter press
			entry1.bind('<Return>', lambda e, cell=cell: key_r(e, cell))

dict['A1'].focus()
