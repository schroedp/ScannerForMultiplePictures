from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog


window = Tk()

window.title("ScannerForMultiplePictures")

window.geometry('300x400')

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
combo.pack(anchor=W, pady=(0,15))

#Radiobutton to choose quality
label = Label(text="Image Quality")
label.pack(anchor=W)

rad1 = Radiobutton(window,text='Low', value=1)
rad2 = Radiobutton(window,text='Middle', value=2)
rad3 = Radiobutton(window,text='High', value=3)

rad1.pack(anchor=W, ipady=5)
rad2.pack(anchor=W, ipady=5)
rad3.pack(anchor=W, ipady=5)

#progressbar
label = Label(text="Progress")
label.pack(anchor=W, pady=(30,0))
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.pack(anchor=W)

#Start button
B = Button(text ="Start")
B.pack(pady=(50,0), padx=15)


#fileinput
#file = filedialog.askopenfilename()
window.mainloop()