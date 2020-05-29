from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog

window = Tk()

window.title("ScannerForMultiplePictures")

window.geometry('300x400')
window.minsize(300, 400)


def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("tiff files","*.tiff"),("All files","*.*")))
    ent1.insert(END, filename)

#Checkbutton for expert mode
chk_state = BooleanVar()
chk_state.set(False) #set check state
chk = Checkbutton(window, text='Expert mode', var=chk_state)
chk.pack(anchor=W, ipady=5, pady=(0,15))

#combobox widget to choose the scanner

label = Label(text="Scanner")
label.pack(anchor=W)
combo = Combobox(window)

combo['values']= ("Scanner1", "Scanner2", "Scanner3")
combo.current(1) #set the selected item
combo.pack(anchor=W, pady=(5,15))

#Radiobutton to choose quality
label = Label(text="Image Quality")
label.pack(anchor=W)

rad1 = Radiobutton(window,text='Low', value=1)
rad2 = Radiobutton(window,text='Middle', value=2)
rad3 = Radiobutton(window,text='High', value=3)

rad1.pack(anchor=W, ipady=3)
rad2.pack(anchor=W, ipady=3)
rad3.pack(anchor=W, ipady=3)

label = Label(window,text="Progress")
label.pack(anchor=W, pady=(15,0))
style = ttk.Style()
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.pack(anchor=W, pady=(5,0))

#fileinput
f1 = Frame(window)
f1.pack(anchor=W, pady=(30,0))


b1=Button(f1,text="Save to...",command=browsefunc)
b1.pack(side=LEFT)

ent1=Entry(f1)
ent1.pack(side=LEFT,ipadx=20)

window.mainloop()