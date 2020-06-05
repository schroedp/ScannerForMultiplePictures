from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
import sys

class ScannerGui():
    def __init__(self):

        self.window = Tk()
        self.window.geometry('300x400')
        self.window.minsize(300, 400)

        self.masterFrame = Frame(self.window)
        self.masterFrame.pack(padx=(20, 20), pady=(5, 5), expand=1, fill=BOTH)

        # Checkbutton for expert mode
        self.exportValue = BooleanVar()
        self.exportValue.set(False)  # set check state
        self.expert = Checkbutton(self.masterFrame, text='Expert mode', var=self.exportValue, command=lambda: self.showexpertmode())
        self.expert.pack(anchor=W, ipady=5, pady=(0, 10), expand=1, fill=BOTH)
        #self.expert.config(font=("Courier", 20))

        # combobox widget to choose the scanner
        self.scannerlabel = Label(self.masterFrame, text="Scanner")
        self.scannerlabel.pack(anchor=W, expand=1, fill=BOTH)
        self.combo = Combobox(self.masterFrame)

        self.combo['values'] = ("Scanner1", "Scanner2", "Scanner3")
        self.combo.current(1)  # set the selected item
        self.combo.pack(anchor=W, pady=(5, 10), expand=1, fill=BOTH)

        # Radiobutton to choose quality
        self.qualitylabel = Label(self.masterFrame, text="Image Quality")

        self.qualityrad1 = Radiobutton(self.masterFrame, text='Low', value=1)
        self.qualityrad2 = Radiobutton(self.masterFrame, text='Middle', value=2)
        self.qualityrad3 = Radiobutton(self.masterFrame, text='High', value=3)

        # fileinput
        self.fileinput = Frame(self.masterFrame)
        self.fileinput.pack(anchor=W, pady=(10, 0), expand=1, fill=BOTH)

        self.uploadButton = Button(self.fileinput, text="Save to...", command=self.browsefunc)
        self.uploadButton.pack(side=LEFT, expand=1, fill=BOTH)

        self.filepath = Entry(self.fileinput)
        self.filepath.pack(side=LEFT, ipadx=20, expand=1, fill=BOTH)

        # progressbar
        self.progressbarlabel = Label(self.masterFrame, text="Progress")
        self.progressbarlabel.pack(anchor=W, pady=(15, 0), expand=1, fill=BOTH)

        self.progressbarstyle = ttk.Style()
        self.progressbarstyle.configure("black.Horizontal.TProgressbar", background='black')
        self.progressbar = Progressbar(self.masterFrame, length=200, style='black.Horizontal.TProgressbar')
        self.progressbar['value'] = 70
        self.progressbar.pack(anchor=W, pady=(5, 0), expand=1, fill=BOTH)

        #Start button
        self.startButton = Button(self.masterFrame, text ="Start",command=self.start)
        self.startButton.pack(anchor=W, pady=(35,0), padx=100, expand=1, fill=BOTH)

        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def showexpertmode(self):
        if self.exportValue.get() == TRUE:
            self.startButton.pack_forget()
            self.qualitylabel.pack(anchor=W, expand=1)
            self.qualityrad1.pack(anchor=W, ipady=3, expand=1, fill=BOTH)
            self.qualityrad2.pack(anchor=W, ipady=3, expand=1, fill=BOTH)
            self.qualityrad3.pack(anchor=W, ipady=3, expand=1, fill=BOTH)
            self.startButton.pack(anchor=W, pady=(35,0), padx=100, expand=1, fill=BOTH)
            self.window.geometry('300x450')
        else:
            self.qualitylabel.pack_forget()
            self.qualityrad1.pack_forget()
            self.qualityrad2.pack_forget()
            self.qualityrad3.pack_forget()
            self.window.geometry('300x400')
            self.window.update()

    def browsefunc(self):
        filename = filedialog.askopenfilename(filetypes=(("tiff files", "*.tiff"), ("All files", "*.*")))
        self.filepath.insert(END, filename)

    def start(self):
        sys.exit()


app = ScannerGui()




