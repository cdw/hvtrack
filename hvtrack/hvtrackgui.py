#!/usr/bin/env python
# encoding: utf-8
"""
hvtrackgui.py - initial stab at tracker gui

Created by Dave Williams on 2014-04-21
"""

import Tkinter as tk
import ttk
import tkFileDialog

class Interface(ttk.Frame):
    """Subclassed interface to the rest of the program
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()   #start it up
        ## Next bits are the GUI state
        self.filename = None
        self.directory = None
        
    def initUI(self):
        self.parent.title("Track video")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        quitButton = ttk.Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=tk.RIGHT, padx=5, pady=5)
        openButton = ttk.Button(self, text="File", command=self.askOpen)
        openButton.pack(side=tk.RIGHT, padx=5, pady=5)
        openButton = ttk.Button(self, text="Directory", command=self.askDir)
        openButton.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def askOpen(self):
        fname = tkFileDialog.askopenfilename()
        print fname
    
    def askDir(self):
        pass


def main():
    root = tk.Tk()
    #root.geometry("350x100+300+300")
    app = Interface(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
