from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.ttk import Progressbar


class ScannerGui():
    def __init__(self):
        self.root = Tk()

        self.root.title("ScannerForMultiplePictures")

        self.root.geometry('300x400')

        # Checkbutton for expert mode
        self.exportValue = BooleanVar()
        self.exportValue.set(False)  # set check state
        self.expert = Checkbutton(self.root, text='Expert mode', var=self.exportValue, command=lambda: self.showexpertmode())
        self.expert.pack(anchor=W, ipady=5, pady=(0, 15))

        self.quality = Label(text="Farbqualität")
        self.qualityValues = Combobox(self.root)

        self.qualityValues['values'] = ("Scanner1", "Scanner2", "Scanner3")
        self.qualityValues.current(1)  # set the selected item

        # combobox widget to choose the scanner

        label = Label(text="Scanner")
        label.pack(anchor=W)
        combo = Combobox(self.root)

        combo['values'] = ("Scanner1", "Scanner2", "Scanner3")
        combo.current(1)  # set the selected item
        combo.pack(anchor=W, pady=(0, 15))

        # Radiobutton to choose quality
        label = Label(text="Image Quality")
        label.pack(anchor=W)

        rad1 = Radiobutton(self.root, text='Low', value=1)
        rad2 = Radiobutton(self.root, text='Middle', value=2)
        rad3 = Radiobutton(self.root, text='High', value=3)

        rad1.pack(anchor=W, ipady=5)
        rad2.pack(anchor=W, ipady=5)
        rad3.pack(anchor=W, ipady=5)

        # progressbar
        label = Label(text="Progress")
        label.pack(anchor=W, pady=(30, 0))
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        bar = Progressbar(self.root, length=200, style='black.Horizontal.TProgressbar')
        bar['value'] = 70
        bar.pack(anchor=W)

        # Start button
        self.B = Button(text="Start")
        self.B.pack(pady=(50, 0), padx=15)

        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def showexpertmode(self):
        if self.exportValue.get() == TRUE:
            self.B.pack_forget()
            self.quality.pack(anchor=W, ipady=5, pady=(40, 0))
            self.qualityValues.pack(anchor=W, ipady=5)
            self.B.pack(pady=(60, 0), padx=15)
            self.root.geometry('300x500')
        else:
            self.quality.pack_forget()
            self.qualityValues.pack_forget()
            self.root.geometry('300x400')
            self.root.update()


app = ScannerGui()






