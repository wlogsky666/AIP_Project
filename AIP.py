import Tkinter as tk
import tkFileDialog
from PIL import ImageTk, Image



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
		return self.weight/size if self.weight > self.height else self.height/size
	def getTKImage(self, size):
		return ImageTk.PhotoImage(self.img.resize((int(self.weight/self.percentageOfSize(size)), int(self.weight/self.percentageOfSize(size))), Image.ANTIALIAS))

srcimg, desimg = IMAGE(), IMAGE()

options = {'initialdir' : '/home/Wlogsky/Pictures', 'defaultextension' : '.jpg'}
defaultFileName = '/home/Wlogsky/Pictures/?.jpg'

win = tk.Tk()
win.title('Show')
win.geometry('1080x720')

srcimg.load(defaultFileName)
tsimg = srcimg.getTKImage(500.0)
srcpanel = tk.Label(win, image=tsimg)
srcpanel.place(x=30, y=150, width=500, height=500)
print(srcimg.img.histogram())

desimg.load(defaultFileName)
tdimg = desimg.getTKImage(500.0)
despanel = tk.Label(win, image=tdimg)
despanel.place(x=550, y=150, width=500, height=500)


def load():
	options['multiple'] = True
	options['title'] = "tkFileDialog.askopenfilename"
	options['filetypes'] = [("jpg","*.jpg"), ("bmp", "*.bmp"), ("ppm", "*.ppm"), ("allfiles","*")]
	file = tkFileDialog.askopenfilename(**options)
	if not file:
		return

	srcimg.load(file[0])
	tsimg = srcimg.getTKImage(500.0)
	srcpanel.configure(image=tsimg)
    	srcpanel.image = tsimg

    	desimg.load(file[0])
	tdimg = ImageTk.PhotoImage(desimg.img.resize((int(desimg.weight/desimg.percentageOfSize(500.0)), int(desimg.weight/desimg.percentageOfSize(500.0))), Image.ANTIALIAS))
    	despanel.configure(image=tdimg)
    	despanel.image = tdimg

def save():
	try:
		del options['multiple']
	except:
		pass
	options['title'] = "tkFileDialog.asksaveasfilename"
	options['filetypes'] = [("jpg","*.jpg")]
	file = tkFileDialog.asksaveasfilename(**options)
	if not file:
		options['multiple'] = True		
		return
	desimg.save(file)


menu = tk.Menu(win, tearoff=0)
menu.add_command(label='Exit', command=win.quit)
menu.add_separator()
menu.add_command(label='Load', command=load)
menu.add_command(label='Save', command=save)

win.config(menu=menu)


win.mainloop()