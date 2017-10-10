import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np


class IMAGE():
	def __init__(self, filename=None):
		self.img = None
		self.filename = None
		self.weight = 0
		self.height = 0	
		if filename is not None:
			self.load(filename)
			self.filename = filename
	def load(self, filename):
		if not self.isNull():
			self.img.close()
		self.img = Image.open(filename)
		self.weight, self.height = self.img.size
	def save(self, filename):
		self.img.save(filename, format='jpeg')
	def percentageOfSize(self, size):
		return self.weight/float(size) if self.weight > self.height else self.height/float(size)
	def getTKImage(self, size):
		return ImageTk.PhotoImage(self.img.resize((int(self.weight/self.percentageOfSize(size)), int(self.height/self.percentageOfSize(size))), Image.ANTIALIAS))
	def isNull(self):
		return self.img is None

srcimg, desimg = IMAGE(), IMAGE()

options = {'initialdir' : '.', 'defaultextension' : '.jpg'}
defaultFileName = './car2.jpg'

win = tk.Tk()
win.title('AIP 60647003S')
win.geometry('1080x720')

srcpanel = tk.Label(win)
srcpanel.place(x=30, y=150, width=500, height=500)
despanel = tk.Label(win)
despanel.place(x=550, y=150, width=500, height=500)

canvas = None
def resetCanvas():
	global canvas
	if canvas != None:
		canvas.get_tk_widget().destroy()
		canvas = None


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

	resetCanvas()

	size = tk.Label(win, text="%dx%d" % ( srcimg.weight, srcimg.height ), font=("Helvetica", 16))
	size.place(x=10, y=680 , width=100)

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

def reload():
	resetCanvas()
	if srcimg.filename is not None:
		load(srcimg.filename)


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

def pressHist():
	if srcimg.isNull() :
		return 
	blackimg = srcimg.img.convert('L')
	y = [0]*255
	for i in range(srcimg.weight):
		for j in range(srcimg.height):
			y[blackimg.getpixel((i, j))-1] += 1

	x = np.arange(0, 255)
	fig=plt.figure(figsize=(500.0/96, 500.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.bar(x, y, linewidth=0, width=1.2, color='black')
	ax.set_xlabel('Intensity')
	ax.set_ylabel('Frequency')
	plt.ylim(0, srcimg.weight*srcimg.height/75)
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=550, y=150, width=500, height=500)
	canvas.show()

def pressNoise():
	pass

histImg, noiseImg = IMAGE('histimg.jpg'), IMAGE('noise.jpg')
histImgTmp = histImg.getTKImage(70.0)
noiseImgTmp = noiseImg.getTKImage(70.0)
histButton = tk.Button(win, command=pressHist, bg='cyan', activebackground='red', image=histImgTmp)
noiseButton = tk.Button(win, command=pressNoise, bg='cyan', activebackground='red', image=noiseImgTmp)
histButton.image = histImgTmp
noiseButton.image = noiseImgTmp
histButton.place(x=30, y=30, width=80, height=80)
noiseButton.place(x=130, y=30, width=80, height=80)

win.mainloop()
