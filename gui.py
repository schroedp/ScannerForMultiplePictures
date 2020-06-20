from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter.ttk import *
from tkinter.ttk import Progressbar
import sys
import time
from extractor import Extractor
import cv2

#TODO Schriftgroesse, Abstaende(fill)
from scanner.scan import scanner


class ScannerGui():
    mode = None
    resolution = None
    brightness = None
    contrast = None
    depth = None

    def __init__(self):
        self.initializeScanner()

        self.window = Tk()
        self.window.title("SCANNERGY")
        self.window.geometry('300x350')
        self.window.minsize(300, 350)
        self.window.maxsize(1500, 800)

        fontStyle = tkFont.Font(size=12)

        self.masterFrame = Frame(self.window)
        self.masterFrame.pack(padx=(20, 20), pady=(20, 20), expand=0, fill=BOTH)

        # Checkbutton for expert mode
        self.exportValue = BooleanVar()
        self.exportValue.set(False)  # set check state
        self.expert = Checkbutton(self.masterFrame, text='Expert mode', var=self.exportValue, command=lambda: self.showexpertmode())
        self.expert.pack(anchor=W, pady=(0, 18), expand=1, fill=X)

        # combobox widget to choose the scanner
        self.scannerlabel = Label(self.masterFrame, text="Choose scanner", font=fontStyle)
        self.scannerlabel.pack(anchor=W, expand=0, fill=X)
        
        self.combo = Combobox(self.masterFrame)
        self.combo.bind("<<ComboboxSelected>>", self.changeScanner)
        device_descriptors = self.scanner.get_device_descriptors(self.scannerapi)
        self.devices = {}
        for device_descriptor in device_descriptors:
            self.devices[self.scanner.get_device_name(device_descriptor)] = device_descriptor

        self.combo['values'] = list(self.devices.keys())
        if len(self.devices) > 0:
            self.combo.current(0)# set the selected item

        self.combo.pack(anchor=W, pady=(5, 18), expand=0, fill=X)

        # scan source selection
        self.sourcelabel = Label(self.masterFrame, text="Choose scanner type", font=fontStyle)
        self.sourcelabel.pack(anchor=W, expand=0, fill=X)

        self.scanSources = Combobox(self.masterFrame)
        self.scanSources.bind("<<ComboboxSelected>>", self.updateOptions)
        try:
            selected_device_descriptor = self.devices[self.combo.get()]
            selected_device = self.scanner.get_device_object(self.scannerapi, selected_device_descriptor)
            sources = self.scanner.get_scan_sources(selected_device)
            self.sourceNames = {}
            for source in sources:
                self.sourceNames[source.get_name()] = source

            self.scanSources['values'] = list(self.sourceNames.keys())
            if len(self.sourceNames) > 0:
                self.scanSources.current(0)
        except:
            print("Error, no Scanner")

        self.scanSources.pack(anchor=W, pady=(5, 18), expand=0, fill=X)

        # fileinput
        self.fileinputlabel = Label(self.masterFrame, text="Choose directory to save pictures", font=fontStyle)
        self.fileinputlabel.pack(anchor=W, expand=0, fill=X)

        self.fileinput = Frame(self.masterFrame)
        self.fileinput.pack(anchor=W, pady=(5, 0), expand=0, fill=X)

        self.saveButton = Button(self.fileinput, text="Save to...", command=self.browsefunc)
        self.saveButton.pack(side=LEFT)

        self.filepath = Entry(self.fileinput)
        self.filepath.pack(side=LEFT, ipadx=20, expand=1, fill=X)

        # progressbar
        self.progressbarlabel = Label(self.masterFrame, text="Scan progress", font=fontStyle)
        
        self.progressbarstyle = ttk.Style()
        self.progressbarstyle.configure("black.Horizontal.TProgressbar", background='black')
        self.progressbar = Progressbar(self.masterFrame, length=200, style='black.Horizontal.TProgressbar')
        self.progressbar['value'] = 0

        self.brightnesslabel = Label(self.masterFrame, text="Brightness", font=fontStyle)
        ScannerGui.brightness = Scale(self.masterFrame, from_=0, to=200, orient=HORIZONTAL)
        self.contrastlabel = Label(self.masterFrame, text="Contrast", font=fontStyle)
        ScannerGui.contrast = Scale(self.masterFrame, from_=0, to=200, orient=HORIZONTAL)
        self.resolutionlabel = Label(self.masterFrame, text="Resolution", font=fontStyle)
        ScannerGui.resolution = Combobox(self.masterFrame)
        self.modelabel = Label(self.masterFrame, text="Color Mode", font=fontStyle)
        ScannerGui.mode = Combobox(self.masterFrame)
        self.depthlabel = Label(self.masterFrame, text="Color Depth", font=fontStyle)
        ScannerGui.depth = Combobox(self.masterFrame)

        #Start button
        self.startButton = Button(self.masterFrame, text="Start", command=self.start)
        self.startButton.pack(anchor=CENTER, pady=(35,0))

        self.updateOptions(None)

        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def showexpertmode(self):
        if self.exportValue.get() == TRUE:
            self.startButton.pack_forget()
            self.progressbarlabel.forget()
            self.progressbar.forget()
            self.progressbar['value'] = 0
            self.brightnesslabel.pack(anchor=W, pady=(18,5), expand=0, fill=X)
            ScannerGui.brightness.pack(anchor=W, expand=0, fill=X)
            self.contrastlabel.pack(anchor=W, pady=(10,5), expand=0, fill=X)
            ScannerGui.contrast.pack(anchor=W, expand=0, fill=X)
            self.resolutionlabel.pack(anchor=W,pady=(10,5), expand=0, fill=X)
            ScannerGui.resolution.pack(anchor=W, expand=0, fill=X)
            self.modelabel.pack(anchor=W,pady=(10,5), expand=0, fill=X)
            ScannerGui.mode.pack(anchor=W, expand=0, fill=X)
            self.depthlabel.pack(anchor=W,pady=(10,0), expand=0, fill=X)
            ScannerGui.depth.pack(anchor=W, expand=0, fill=X)
            self.startButton.pack(anchor=CENTER, pady=(35,0))
            self.window.geometry('300x650')

        else:
            self.brightness.pack_forget()
            self.contrast.pack_forget()
            self.resolution.pack_forget()
            self.mode.pack_forget()
            self.depth.pack_forget()
            self.brightnesslabel.pack_forget()
            self.depthlabel.pack_forget()
            self.resolutionlabel.pack_forget()
            self.modelabel.pack_forget()
            self.contrastlabel.pack_forget()
            self.progressbarlabel.forget()
            self.progressbar.forget()
            self.progressbar['value'] = 0
            self.startButton.forget()
            self.startButton.pack(anchor=CENTER, pady=(35,0))
            self.window.geometry('300x350')
            self.window.update()

    def browsefunc(self):
        filename = filedialog.askdirectory()
        self.filepath.insert(END, filename)

    def start(self):
        self.startButton.pack_forget()
        self.progressbarlabel.pack(anchor=W, pady=(18, 5), expand=0, fill=X)
        self.progressbar.pack(anchor=W, expand=0, fill=X)
        self.startButton.pack(anchor=CENTER, pady=(35,0))
        try: 
            print(ScannerGui.mode.get())
            self.scanner.set_option(self.sourceNames[self.scanSources.get()], "mode", ScannerGui.mode.get())
            self.scanner.set_option(self.sourceNames[self.scanSources.get()], "resolution", ScannerGui.resolution.get())
            self.scanner.set_option(self.sourceNames[self.scanSources.get()], "brightness", ScannerGui.brightness.get())
            print(ScannerGui.brightness.get())
            self.scanner.set_option(self.sourceNames[self.scanSources.get()], "contrast", ScannerGui.contrast.get())
            print(ScannerGui.contrast.get())
            self.scanner.set_option(self.sourceNames[self.scanSources.get()], "depth", ScannerGui.depth.get())
            #self.scanner.set_option(self.sourceNames[self.scanSources.get()], "dps_page_size", "iso_a4")
            self.scanner.scan(self.sourceNames[self.scanSources.get()], "./temp.png")

            extracted = Extractor(".", True).extract(cv2.imread("./temp.png"))
            print("Extracted " + extracted + " Images.")

        except:
            print("Error, no Scanner")


        if self.exportValue.get() == TRUE:
            self.window.geometry('300x700')
        else:
            self.window.geometry('300x400')
        

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

    def changeScanner(self, event):
        try:
            selected_device_descriptor = self.devices[self.combo.get()]
            selected_device = self.scanner.get_device_object(self.scannerapi, selected_device_descriptor)
            sources = self.scanner.get_scan_sources(selected_device)
            sourceNames = {}
            for source in sources:
                sourceNames[source.get_name()] = source

            self.scanSources['values'] = list(sourceNames.keys())
            if len(sourceNames) > 0:
                self.scanSources.current(0)
        except:
            print("Error, no Scanner")

    def updateOptions(self, event):
        try: 
            selectedSource = self.sourceNames[self.scanSources.get()]
            options = self.scanner.get_options(selectedSource)

            self.optionNames = {}
            for option in options:
                self.optionNames[option.get_name()] = option
                try:
                    attribute = getattr(self, option.get_name())
                    if attribute is not None:
                        if isinstance(attribute, Scale):
                            attribute.configure(to=option.get_constraint()[1])
                            attribute.configure(from_=option.get_constraint()[0])
                            attribute.set(option.get_value())
                        else:
                            attribute['values'] = option.get_constraint()
                            attribute.current(option.get_constraint().index(option.get_value()))
                            print(attribute)
                except AttributeError as error:
                    print(error)
        except:
            print("Error, no Scanner")

app = ScannerGui()




