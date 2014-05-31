#!/usr/bin/env python
# encoding: utf-8
"""
hvtrackgui.py - initial stab at tracker gui

Created by Dave Williams on 2014-04-21
"""

import Tkinter as tk
import ttk
import tkFileDialog
import hummertracker
import os


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
        """Put all the UI widgets where they go"""
        self.parent.title("Track video")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        # Create subframes to contain each section
        self.video_f = ttk.Frame(self.parent)
        self.video_f.pack(side=tk.TOP)
        self.segment_f = ttk.Frame(self.parent)
        self.segment_f.pack(side=tk.BOTTOM)
        self.contour_f = ttk.Frame(self.parent)
        self.contour_f.pack(side=tk.BOTTOM)
        self.path_f = ttk.Frame(self.parent)
        self.path_f.pack(side=tk.BOTTOM)
        #Video
        videoLabel = ttk.Label(self.video_f, text="Video")
        videoLabel.pack(side=tk.TOP, padx=5, pady=5)
        quitButton = ttk.Button(self.video_f, text="Quit", command=self.quit)
        quitButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        openButton = ttk.Button(self.video_f, text="File", command=self.askOpen)
        openButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        openButton = ttk.Button(self.video_f, text="Dir", command=self.askDir)
        openButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        segmentLabel = ttk.Label(self.segment_f, text="Foreground segmentation")
        segmentLabel.pack(side=tk.TOP, padx=5, pady=5)
        threshLabel = ttk.Label(self.segment_f, text="Threshold Area")
        threshLabel.pack(side=tk.BOTTOM, padx=5, pady=5)
    
    def askOpen(self):
        """Ask for a file, then run the tracker on it"""
        fname = tkFileDialog.askopenfilename()
        trace = hummertracker.vid_to_trace(fname) #throwing PIL error, need to
        #track down
        hummertracker.save_trace(os.path.splitext(fname)[0] + '.pkl')
        print fname
    
    def askDir(self):
        """Ask for a directory, then run the tracker on it"""
        dirname = tkFileDialog.askdirectory()
        hummertracker.dir_to_traces(dirname)
        print dirname

def main():
    root = tk.Tk()
    #root.geometry("350x100+300+300")
    app = Interface(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
