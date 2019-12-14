import json

from element_compiler import tkinter, Compiler


class Engine:
    root = tkinter.Tk()
    
    def __init__(self, mainFrame):
        self.root.attributes("-fullscreen", True) 
        self.root.title("LogBrowser")

        self.mainFrame = Compiler.createElement(mainFrame)

    def run(self):
        self.root.mainloop()