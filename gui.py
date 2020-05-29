from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
import sys

window = Tk()

window.title("ScannerForMultiplePictures")

window.geometry('300x400')
window.minsize(300, 400)

masterFrame = Frame(window)
masterFrame.pack(padx=(20,20), pady=(5,5), expand=1, fill=BOTH)

def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("tiff files","*.tiff"),("All files","*.*")))
    ent1.insert(END, filename)

def start():
    sys.exit()

#Checkbutton for expert mode
chk_state = BooleanVar()
chk_state.set(False) #set check state
chk = Checkbutton(masterFrame, text='Expert mode', var=chk_state)
chk.pack(anchor=W, ipady=5, pady=(0,15), expand=1, fill=BOTH)
chk.config(font=("Courier", 20))

#combobox widget to choose the scanner
label = Label(masterFrame, text="Scanner")
label.pack(anchor=W, expand=1, fill=BOTH)
combo = Combobox(masterFrame)

combo['values']= ("Scanner1", "Scanner2", "Scanner3")
combo.current(1) #set the selected item
combo.pack(anchor=W, pady=(5,15), expand=1, fill=BOTH)

#Radiobutton to choose quality
label = Label(masterFrame, text="Image Quality")
label.pack(anchor=W, expand=1)

rad1 = Radiobutton(masterFrame,text='Low', value=1)
rad2 = Radiobutton(masterFrame,text='Middle', value=2)
rad3 = Radiobutton(masterFrame,text='High', value=3)

rad1.pack(anchor=W, ipady=3, expand=1, fill=BOTH)
rad2.pack(anchor=W, ipady=3, expand=1, fill=BOTH)
rad3.pack(anchor=W, ipady=3, expand=1, fill=BOTH)

#fileinput
f1 = Frame(masterFrame)
f1.pack(anchor=W, pady=(20,0), expand=1, fill=BOTH)

b1=Button(f1,text="Save to...",command=browsefunc)
b1.pack(side=LEFT, expand=1, fill=BOTH)

ent1=Entry(f1)
ent1.pack(side=LEFT,ipadx=20, expand=1, fill=BOTH)

#progressbar
label = Label(masterFrame,text="Progress")
label.pack(anchor=W, pady=(15,0), expand=1, fill=BOTH)

style = ttk.Style()
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(masterFrame, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.pack(anchor=W, pady=(5,0), expand=1, fill=BOTH)

#Start button
B = Button(masterFrame, text ="Start",command=start)
B.pack(anchor=W, pady=(35,0), padx=100, expand=1, fill=BOTH)

window.mainloop()
