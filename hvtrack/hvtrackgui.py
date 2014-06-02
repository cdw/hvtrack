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
    """Subclassed interface to the rest of the program."""
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
        self.video_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                          fill=tk.BOTH, ipadx=10, ipady=10)
        self.segment_f = ttk.Frame(self.parent)
        self.segment_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                            fill=tk.BOTH, ipadx=10, ipady=10)
        self.contour_f = ttk.Frame(self.parent)
        self.contour_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                            fill=tk.BOTH, ipadx=10, ipady=10)
        self.path_f = ttk.Frame(self.parent)
        self.path_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                         fill=tk.BOTH, ipadx=10, ipady=10)
        #Quit
        quitButton = ttk.Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        #Video
        videoLabel = ttk.Label(self.video_f, text="Video")
        fileLabel = ttk.Label(self.video_f, text="File:")
        fileEntry = ttk.Entry(self.video_f, width=30)
        fileButton = ttk.Button(self.video_f, text="File", command=self.askOpen)
        dirLabel = ttk.Label(self.video_f, text="Directory:")
        dirEntry = ttk.Entry(self.video_f, width=30)
        dirButton = ttk.Button(self.video_f, text="Dir", command=self.askDir)
        #openButton = ttk.Button(self.video_f, text="File", command=self.askOpen)
        #openButton = ttk.Button(self.video_f, text="Dir", command=self.askDir)
        #videoLabel.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        #openButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        #openButton.pack(side=tk.BOTTOM, padx=5, pady=5)
        videoLabel.grid(row=1, column=1, padx=5, pady=15,
                        columnspan=3, sticky=tk.W)
        fileLabel.grid(row=2, column=1, padx=5, pady=5)
        fileEntry.grid(row=2, column=2, padx=5, pady=5)
        fileButton.grid(row=2, column=3, padx=5, pady=5)
        dirLabel.grid(row=3, column=1, padx=5, pady=5)
        dirEntry.grid(row=3, column=2, padx=5, pady=5)
        dirButton.grid(row=3, column=3, padx=5, pady=5)
        #Segmentation
        segmentLabel = ttk.Label(self.segment_f, text="Foreground segmentation")
        #segmentLabel.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        threshLabel = ttk.Label(self.segment_f, text="Threshold Area")
        threshEntry = ttk.Entry(self.segment_f, width=7)
        openxLabel = ttk.Label(self.segment_f, text="Opening X")
        openxEntry = ttk.Entry(self.segment_f, width=7)
        openyLabel = ttk.Label(self.segment_f, text="Opening Y")
        openyEntry = ttk.Entry(self.segment_f, width=7)
        segmentLabel.grid(row=1, column=1, padx=5, pady=15,
                          columnspan=3, sticky=tk.W)
        threshLabel.grid(row=2, column=1, padx=5, pady=5)
        threshEntry.grid(row=2, column=2, padx=5, pady=5)
        openxLabel.grid(row=2, column=3, padx=5, pady=5)
        openxEntry.grid(row=2, column=4, padx=5, pady=5)
        openyLabel.grid(row=2, column=5, padx=5, pady=5)
        openyEntry.grid(row=2, column=6, padx=5, pady=5)
        #Contour
        contourLabel = ttk.Label(self.contour_f, text="Contour filtering")
        c_area_minLabel = ttk.Label(self.contour_f, text="Min area")
        c_area_minEntry = ttk.Entry(self.contour_f, width=10)
        c_area_maxLabel = ttk.Label(self.contour_f, text="Max area")
        c_area_maxEntry = ttk.Entry(self.contour_f, width=10)
        c_perim_minLabel = ttk.Label(self.contour_f, text="Min perim")
        c_perim_minEntry = ttk.Entry(self.contour_f, width=10)
        c_perim_maxLabel = ttk.Label(self.contour_f, text="Max perim")
        c_perim_maxEntry = ttk.Entry(self.contour_f, width=10)
        c_ratio_minLabel = ttk.Label(self.contour_f, text="Min ratio")
        c_ratio_minEntry = ttk.Entry(self.contour_f, width=10)
        c_ratio_maxLabel = ttk.Label(self.contour_f, text="Max ratio")
        c_ratio_maxEntry = ttk.Entry(self.contour_f, width=10)
        contourLabel.grid(row=1, column=1, padx=5, pady=15,
                          columnspan=3, sticky=tk.W)
        c_area_minLabel.grid(row=2, column=1)
        c_area_minEntry.grid(row=2, column=2)
        c_area_maxLabel.grid(row=2, column=3)
        c_area_maxEntry.grid(row=2, column=4)
        c_perim_minLabel.grid(row=3, column=1)
        c_perim_minEntry.grid(row=3, column=2)
        c_perim_maxLabel.grid(row=3, column=3)
        c_perim_maxEntry.grid(row=3, column=4)
        c_ratio_minLabel.grid(row=4, column=1)
        c_ratio_minEntry.grid(row=4, column=2)
        c_ratio_maxLabel.grid(row=4, column=3)
        c_ratio_maxEntry.grid(row=4, column=4)
        #Path
        pathLabel = ttk.Label(self.path_f, text="Path matching")
        nearLabel = ttk.Label(self.path_f, text="Nearness")
        nearEntry = ttk.Entry(self.path_f, width=10)
        pathLabel.grid(row=1, column=1, padx=5, pady=15,
                       columnspan=2, sticky=tk.W)
        nearLabel.grid(row=2, column=1)
        nearEntry.grid(row=2, column=2)


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
