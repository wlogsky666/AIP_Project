# coding=utf-8
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np
import random
from math import sin, cos, log, pi, sqrt


class IMAGE():
	def __init__(self, filename=None):
		self.img = None
		self.reset()
		if filename is not None:
			self.load(filename)
	def load(self, filename):
		self.reset()
		self.img = Image.open(filename)
		self.width, self.height = self.img.size
		self.filename = filename
	def save(self, filename):
		self.img.save(filename, format='jpeg')
	def percentageOfSize(self, size):
		return self.width/float(size) if self.width > self.height else self.height/float(size)
	def getTKImage(self, size):
		return ImageTk.PhotoImage(self.img.resize((int(self.width/self.percentageOfSize(size)), int(self.height/self.percentageOfSize(size))), Image.ANTIALIAS))
	def isNull(self):
		return self.img is None
	def reset(self):
		if not self.isNull():
			self.img.close()
		self.img = None
		self.filename = None
		self.width, self.height = 0, 0

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

	size = tk.Label(win, text="%dx%d %s" % ( srcimg.width, srcimg.height, srcimg.filename.split('.')[1] ), font=("Helvetica", 16))
	size.place(x=10, y=680 , width=200)

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
	load(srcimg.filename)


try:
	load(defaultFileName)
except:
	pass

def pressHist():
	if srcimg.isNull() :
		return 
	blackimg = srcimg.img.convert('L')
	y = [0]*256
	for i in range(srcimg.width):
		for j in range(srcimg.height):
			y[blackimg.getpixel((i, j))] += 1

	resetCanvas()
	x = np.arange(0, 256)
	fig=plt.figure(figsize=(500.0/96, 500.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.bar(x, y, linewidth=0, width=1.2, color='black')
	ax.set_xlabel('Intensity')
	ax.set_ylabel('Frequency')
	plt.ylim(0, srcimg.width*srcimg.height/75)
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=550, y=150, width=500, height=500)
	canvas.show()

v = tk.StringVar()
noiseInput = tk.Entry(win, textvariable=v, justify='center', font=("Helvetica", 14))
noiseInput.place(x=160, y=115, width=50, height=20)
v.set(50)
l1 = tk.Label(win, text = u'a = ', font=("Helvetica", 14))
l1.place(x=130, y=115, width=30, height=20)

def pressNoise():
	if srcimg.isNull() :
		return 
	srcimg.img = srcimg.img.convert('L')
	𝜎 = int(noiseInput.get())
	print(𝜎)

	hist = []

	for x in range(srcimg.height):
		for y in range(0, srcimg.width-1, 2):
			𝑟, 𝜑 = random.random(), random.random()
			z1 = 𝜎 * cos(2*pi*𝜑) * sqrt(-2*log(𝑟))
			z2 = 𝜎 * sin(2*pi*𝜑) * sqrt(-2*log(𝑟))
			
			fx1 = srcimg.img.getpixel((y, x)) + z1
			fx2 = srcimg.img.getpixel((y+1, x)) + z2

			if fx1 < 0: fx1 = 0 ;
			elif fx1 > 255: fx1 = 255 ;

			if fx2 < 0: fx2 = 0 ;
			elif fx2 > 255: fx2 = 255 ;

			srcimg.img.putpixel((y, x), int(fx1))
			srcimg.img.putpixel((y+1, x), int(fx2))
			hist.append(round(z1, 1))
			hist.append(round(z2, 1))

	# print(hist)
	hist_max = max(hist)
	hist_min = min(hist)

	bins = np.arange(hist_min, hist_max, 0.5)

	resetCanvas()
	fig=plt.figure(figsize=(500.0/96, 500.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.hist(hist, bins=bins, linewidth=0, width=1.2, color='black')
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=550, y=150, width=500, height=500)
	canvas.show()	
	
	tsimg = srcimg.getTKImage(500.0)
	srcpanel.configure(image=tsimg)
	srcpanel.image = tsimg

	desimg.img.close()
	desimg.img = srcimg.img



histImg, noiseImg, reloadImg = IMAGE('histimg.jpg'), IMAGE('noise.jpg'), IMAGE('reload.jpg')
histImgTmp, noiseImgTmp, reloadImgTmp = histImg.getTKImage(70.0), noiseImg.getTKImage(70.0), reloadImg.getTKImage(70.0)
histButton = tk.Button(win, command=pressHist, bg='cyan', activebackground='red', image=histImgTmp)
noiseButton = tk.Button(win, command=pressNoise, bg='cyan', activebackground='red', image=noiseImgTmp)
reloadButton = tk.Button(win, command=reload, bg='cyan', activebackground='red', image=reloadImgTmp)
histButton.image, noiseButton.image, reloadButton.image = histImgTmp, noiseImgTmp, reloadImgTmp
histButton.place(x=30, y=30, width=80, height=80)
noiseButton.place(x=130, y=30, width=80, height=80)
reloadButton.place(x=970, y=30, width=80, height=80)

menu = tk.Menu(win, tearoff=0)
menu.add_command(label='Exit', command=win.quit)
menu.add_separator()
menu.add_command(label='Load', command=load)
menu.add_separator()
menu.add_command(label='Save', command=save)
win.config(menu=menu)

win.mainloop()
win.quit()

