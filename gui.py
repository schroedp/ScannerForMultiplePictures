from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
import sys
import time

#TODO Schriftgroesse, Abstaende(fill)
from scanner.scan import scanner


class ScannerGui():
    def __init__(self):
        self.initializeScanner()

        self.window = Tk()
        self.window.geometry('300x400')
        self.window.minsize(300, 400)

        self.masterFrame = Frame(self.window)
        self.masterFrame.pack(padx=(20, 20), pady=(5, 5), expand=1, fill=BOTH)

        # Checkbutton for expert mode
        self.exportValue = BooleanVar()
        self.exportValue.set(False)  # set check state
        self.expert = Checkbutton(self.masterFrame, text='Expert mode', var=self.exportValue, command=lambda: self.showexpertmode())
        self.expert.pack(anchor=W, expand=1, fill=BOTH)

        # combobox widget to choose the scanner
        self.scannerlabel = Label(self.masterFrame, text="Scanner")
        self.scannerlabel.pack(anchor=W, expand=1, fill=BOTH)
        
        self.combo = Combobox(self.masterFrame)
        device_descriptors = self.scanner.get_device_descriptors(self.scannerapi)#
        self.devices = {}
        for device_descriptor in device_descriptors:
            self.devices[self.scanner.get_device_name(device_descriptor)] = device_descriptor

        self.combo['values'] = list(self.devices.keys())
        if len(self.devices) > 0:
            self.combo.current(0)# set the selected item

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
        
        self.progressbarstyle = ttk.Style()
        self.progressbarstyle.configure("black.Horizontal.TProgressbar", background='black')
        self.progressbar = Progressbar(self.masterFrame, length=200, style='black.Horizontal.TProgressbar')
        self.progressbar['value'] = 0
        

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
            self.qualityrad1.pack(anchor=W, ipady=1, expand=1, fill=BOTH)
            self.qualityrad2.pack(anchor=W, ipady=1, expand=1, fill=BOTH)
            self.qualityrad3.pack(anchor=W, ipady=1, expand=1, fill=BOTH)
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
        filename = filedialog.askopenfilename(filetypes=(("tiff files, jpeg files, png files", "*.tiff, *.jpeg. *.png"), ("All files", "*.*")))
        self.filepath.insert(END, filename)

    def start(self):
        self.startButton.pack_forget()
        self.progressbarlabel.pack(anchor=W, pady=(15, 0), expand=1, fill=BOTH)
        self.progressbar.pack(anchor=W, expand=1, fill=BOTH)
        self.startButton.pack(anchor=W, pady=(35,0), padx=100, expand=1, fill=BOTH)
        selected_device_descriptor = self.devices[self.combo.get()]
        selected_device = self.scanner.get_device_object(self.scannerapi, selected_device_descriptor)
        sources = self.scanner.get_scan_sources(selected_device)
        self.scanner.scan(sources[0], "C:\\Users\\Technician\\out.png")


        self.window.update()
        time.sleep(1)
        self.progressbar['value'] = 20
        self.window.update()
        time.sleep(1)
        self.progressbar['value'] = 60
        self.window.update()
        time.sleep(1)
        self.progressbar['value'] = 100
        self.window.update()


    def initializeScanner(self):
        self.scanner = scanner()
        self.scannerapi = self.scanner.init_api()


app = ScannerGui()




