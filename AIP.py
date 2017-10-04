import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog


class IMAGE():
	def __init__(self):
		self.img = None
		self.weight = 0
		self.height = 0	
	def load(self, filename):
		if self.img != None:
			self.img.close()
		self.img = Image.open(filename)
		self.weight, self.height = self.img.size
	def save(self, filename):
		self.img.save(filename, format='jpeg')
	def percentageOfSize(self, size):
		return self.weight/float(size) if self.weight > self.height else self.height/float(size)
	def getTKImage(self, size):
		return ImageTk.PhotoImage(self.img.resize((int(self.weight/self.percentageOfSize(size)), int(self.height/self.percentageOfSize(size))), Image.ANTIALIAS))

srcimg, desimg = IMAGE(), IMAGE()

options = {'initialdir' : '.', 'defaultextension' : '.jpg'}
defaultFileName = './car2.jpg'

win = tk.Tk()
win.title('Show')
win.geometry('1080x720')

srcpanel = tk.Label(win)
srcpanel.place(x=30, y=150, width=500, height=500)
despanel = tk.Label(win)
despanel.place(x=550, y=150, width=500, height=500)

def load(filename=None):
	if filename is None:
		options['multiple'] = True
		options['title'] = "tkFileDialog.askopenfilename"
		options['filetypes'] = [("jpg","*.jpg"), ("bmp", "*.bmp"), ("ppm", "*.ppm"), ("allfiles","*")]
		file = filedialog.askopenfilename(**options)
		if not file:
			return
		filename = file[0]

	srcimg.load(filename)
	tsimg = srcimg.getTKImage(500.0)
	srcpanel.configure(image=tsimg)
	srcpanel.image = tsimg


	desimg.load(filename)
	tdimg = desimg.getTKImage(500.0)
	despanel.configure(image=tdimg)
	despanel.image = tdimg

def save():
	try:
		del options['multiple']
	except:
		pass
	options['title'] = "tkFileDialog.asksaveasfilename"
	options['filetypes'] = [("jpg","*.jpg")]
	file = filedialog.asksaveasfilename(**options)
	if not file:
		options['multiple'] = True		
		return
	desimg.save(file)

try:
	load(defaultFileName)
except:
	pass

menu = tk.Menu(win, tearoff=0)
menu.add_command(label='Exit', command=win.quit)
menu.add_separator()
menu.add_command(label='Load', command=load)
menu.add_separator()
menu.add_command(label='Save', command=save)

win.config(menu=menu)
win.mainloop()
