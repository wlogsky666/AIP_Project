# coding=utf-8
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

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
	def __del__(self):
		if self.img is not None:
			self.img.close()
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

def showPanel():
	tsimg = srcimg.getTKImage(500.0)
	srcpanel.configure(image=tsimg)
	srcpanel.image = tsimg

	tdimg = desimg.getTKImage(500.0)
	despanel.configure(image=tdimg)
	despanel.image = tdimg

canvas, canvas1 = None, None
def resetCanvas():
	global canvas, canvas1
	if canvas != None:
		canvas.get_tk_widget().destroy()
		canvas = None
	if canvas1 != None:
		canvas1.get_tk_widget().destroy()
		canvas1 = None


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
	desimg.load(filename)
	showPanel()
	resetCanvas()

	size = tk.Label(win, text="%dx%d %s" % ( srcimg.width, srcimg.height, srcimg.filename.split('.')[1] ), font=("Helvetica", 16))
	size.place(x=10, y=680 , width=200)

def save():
	try:
		del options['multiple']
	except:
		pass
	options['title'] = "tkFileDialog.asksaveasfilename"
	options['filetypes'] = [("jpg", "*.jpg")]
	file = filedialog.asksaveasfilename(**options)
	if not file:
		options['multiple'] = True		
		return
	desimg.save(file)

def reload():
	resetCanvas()
	load(srcimg.filename)


def thous(x, pos):
    return '%1.1fK' % (x*1e-3)

formatter = FuncFormatter(thous)

def pressHist():
	if srcimg.isNull() :
		return 
	blackimg = srcimg.img.convert('L')
	hist = blackimg.getdata()
	bins = np.arange(0, 255, 1)

	resetCanvas()
	fig=plt.figure(figsize=(500.0/96, 500.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.yaxis.set_major_formatter(formatter)
	ax.hist(hist, bins=bins, linewidth=0, width=1.2, color='black')
	ax.set_xlabel('Intensity')
	ax.set_ylabel('Frequency')
	ax.set_xticks(np.arange(0, 255 ,20))
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=550, y=150, width=500, height=500)
	canvas.show()	

## For noise 𝜎 value
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

	hist = list()

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

	bins = np.arange(-200, 200, 1)

	resetCanvas()
	fig=plt.figure(figsize=(500.0/96, 500.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.hist(hist, bins=bins, linewidth=0, width=1.2, color='black')
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=550, y=150, width=500, height=500)
	canvas.show()	
	
	showPanel()

	desimg.img.close()
	desimg.img = srcimg.img

def pressFFT():
	if srcimg.isNull() :
		return 
	srcimg.img = srcimg.img.convert('L')

	pixel = np.asarray(srcimg.img)
	fourier = np.fft.fft2(pixel)
	fourier = abs(np.fft.fftshift(fourier))
	originrange = np.nanmax(fourier[np.isfinite(fourier)]) - np.nanmin(fourier[np.isfinite(fourier)])
	norm = (fourier-np.nanmin(fourier[np.isfinite(fourier)])) * 255 / originrange + 20

	desimg.img.close()
	desimg.img = Image.fromarray(norm).convert('L')

	resetCanvas()
	showPanel()

def pressHistEqual():
	if srcimg.isNull():
		return
	srcimg.img = srcimg.img.convert('L')
	desimg.img = desimg.img.convert('L')

	## Intensity
	H = np.zeros(256)
	for x in range(srcimg.img.height):
		for y in range(srcimg.img.width):
			H[srcimg.img.getpixel((y, x))] += 1

	## Gmin
	gmin = 2000000
	for x in range(256):
		if 0 < H[x]:
			gmin = x
			break 

	## Cumulative 
	Hc = np.zeros(256)
	Hc[0] = H[0]
	for i in range(1, 256):
		Hc[i] = Hc[i-1] + H[i]
	
	Hmin = Hc[gmin] 

	## Tg
	Tg = np.zeros(256)
	for i in range(256):
		Tg[i] = round( (Hc[i]-Hmin)/(srcimg.img.width*srcimg.img.height-Hmin)*255 )

	## Rescan
	for x in range(srcimg.img.height):
		for y in range(srcimg.img.width):
			desimg.img.putpixel((y, x), int(Tg[srcimg.img.getpixel((y,x))]))

	resetCanvas()

	hist = srcimg.img.getdata()
	bins = np.arange(0, 255, 1)
	fig=plt.figure(figsize=(200.0/96, 200.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.hist(hist, bins=bins, linewidth=0, width=1.2, color='black')
	ax.set_xlabel('Intensity')
	ax.set_ylabel('Frequency')
	ax.set_xticks([])
	ax.set_yticks([])
	global canvas
	canvas=FigureCanvasTkAgg(fig, master=win)
	canvas._tkcanvas.place(x=330, y=520, width=200, height=200)
	# plt.yscale('log')

	hist = desimg.img.getdata()

	fig=plt.figure(figsize=(200.0/96, 200.0/96))
	ax=fig.add_axes([0.1,0.1,0.8,0.8], projection='rectilinear')
	ax.hist(hist, bins=bins, linewidth=0, width=1.2, color='black')
	ax.set_xlabel('Intensity')
	ax.set_ylabel('Frequency')
	ax.set_xticks([])
	ax.set_yticks([])
	global canvas1
	canvas1=FigureCanvasTkAgg(fig, master=win)
	canvas1._tkcanvas.place(x=850, y=520, width=200, height=200)

	# plt.yscale('log')
	canvas.show()
	canvas1.show()
	showPanel()



histImg, noiseImg, fftImg, histEqualImg, reloadImg = IMAGE('histimg.jpg'), IMAGE('noise.jpg'),IMAGE('fft.png'), IMAGE('histequal.png'), IMAGE('reload.jpg')
histImgTmp, noiseImgTmp,fftImgTmp, histEqualImgTmp, reloadImgTmp = histImg.getTKImage(70.0), noiseImg.getTKImage(70.0),fftImg.getTKImage(70.0), histEqualImg.getTKImage(70.0), reloadImg.getTKImage(70.0)
histButton = tk.Button(win, command=pressHist, bg='cyan', activebackground='red', image=histImgTmp).place(x=30, y=30, width=80, height=80)
noiseButton = tk.Button(win, command=pressNoise, bg='cyan', activebackground='red', image=noiseImgTmp).place(x=130, y=30, width=80, height=80)
fftButton = tk.Button(win, command=pressFFT, bg='cyan', activebackground='red', image=fftImgTmp).place(x=230, y=30, width=80, height=80)
histEqualButton = tk.Button(win, command=pressHistEqual, bg='cyan', activebackground='red', image=histEqualImgTmp).place(x=330, y=30, width=80, height=80)
reloadButton = tk.Button(win, command=reload, bg='cyan', activebackground='red', image=reloadImgTmp).place(x=970, y=30, width=80, height=80)


menu = tk.Menu(win, tearoff=0)
menu.add_command(label='Exit', command=win.quit)
menu.add_separator()
menu.add_command(label='Load', command=load)
menu.add_separator()
menu.add_command(label='Save', command=save)
win.config(menu=menu)
win.protocol("WM_DELETE_WINDOW", win.quit)

try:
	load(defaultFileName)
except:
	pass

win.mainloop()
