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
# Local imports
import video
import background
import segment
import contour
import path


def disp(input_num_or_none):
    """Numbers returned as integer strings, Nones as blank strings."""
    if input_num_or_none is not None:
        return "%i"%input_num_or_none
    else:
        return ""

class SegmentFrame(ttk.Frame):
    """Configure a segment instance."""
    def __init__(self, parent, segment):
        self.segment = segment  # A passed segment class instance
        ## Gui setup
        ttk.Frame.__init__(self, parent)   
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        segmentLabel = ttk.Label(self, text="Foreground segmentation")
        threshLabel = ttk.Label(self, text="Threshold Area")
        threshEntry = ttk.Entry(self, width=7)
        openxLabel = ttk.Label(self, text="Opening X")
        openxEntry = ttk.Entry(self, width=7)
        openyLabel = ttk.Label(self, text="Opening Y")
        openyEntry = ttk.Entry(self, width=7)
        ## Pack widgets
        segmentLabel.grid(row=1, column=1, padx=5, pady=15,
                          columnspan=3, sticky=tk.W)
        threshLabel.grid(row=2, column=1, padx=5, pady=5)
        threshEntry.grid(row=2, column=2, padx=5, pady=5)
        openxLabel.grid(row=2, column=3, padx=5, pady=5)
        openxEntry.grid(row=2, column=4, padx=5, pady=5)
        openyLabel.grid(row=2, column=5, padx=5, pady=5)
        openyEntry.grid(row=2, column=6, padx=5, pady=5)
        ## Set default values
        threshEntry.delete(0, tk.END)
        threshEntry.insert(0, disp(self.segment.thresh_area))
        openxEntry.delete(0, tk.END)
        openxEntry.insert(0, disp(self.segment.open_kernel_x))
        openyEntry.delete(0, tk.END)
        openyEntry.insert(0, disp(self.segment.open_kernel_y))


class ContourFrame(ttk.Frame):
    """Configure a contour instance."""
    def __init__(self, parent, contour):
        self.contour = contour  # A passed contour class instance
        ttk.Frame.__init__(self, parent)   
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        contour_label = ttk.Label(self, text="Contour filtering")
        area_min_label = ttk.Label(self, text="Min area")
        area_min_entry = ttk.Entry(self, width=10)
        area_max_label = ttk.Label(self, text="Max area")
        area_max_entry = ttk.Entry(self, width=10)
        perim_min_label = ttk.Label(self, text="Min perim")
        perim_min_entry = ttk.Entry(self, width=10)
        perim_max_label = ttk.Label(self, text="Max perim")
        perim_max_entry = ttk.Entry(self, width=10)
        ratio_min_label = ttk.Label(self, text="Min ratio")
        ratio_min_entry = ttk.Entry(self, width=10)
        ratio_max_label = ttk.Label(self, text="Max ratio")
        ratio_max_entry = ttk.Entry(self, width=10)
        ## Pack widgets
        contour_label.grid(row=1, column=1, padx=5, pady=15,
                          columnspan=3, sticky=tk.W)
        area_min_label.grid(row=2, column=1)
        area_min_entry.grid(row=2, column=2)
        area_max_label.grid(row=2, column=3)
        area_max_entry.grid(row=2, column=4)
        perim_min_label.grid(row=3, column=1)
        perim_min_entry.grid(row=3, column=2)
        perim_max_label.grid(row=3, column=3)
        perim_max_entry.grid(row=3, column=4)
        ratio_min_label.grid(row=4, column=1)
        ratio_min_entry.grid(row=4, column=2)
        ratio_max_label.grid(row=4, column=3)
        ratio_max_entry.grid(row=4, column=4)
        # Set default values
        area_min_entry.delete(0, tk.END)
        area_min_entry.insert(0, disp(self.contour.area_min))
        area_max_entry.delete(0, tk.END)
        area_max_entry.insert(0, disp(self.contour.area_max))
        perim_min_entry.delete(0, tk.END)
        perim_min_entry.insert(0, disp(self.contour.perim_min))
        perim_max_entry.delete(0, tk.END)
        perim_max_entry.insert(0, disp(self.contour.perim_max))
        ratio_min_entry.delete(0, tk.END)
        ratio_min_entry.insert(0, disp(self.contour.ratio_min))
        ratio_max_entry.delete(0, tk.END)
        ratio_max_entry.insert(0, disp(self.contour.ratio_max))
        
class PathFrame(ttk.Frame):
    """Configure a path instance."""
    def __init__(self, parent, path):
        self.path = path  # A passed path class instance
        ttk.Frame.__init__(self, parent)   
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        pathLabel = ttk.Label(self, text="Path matching")
        nearLabel = ttk.Label(self, text="Nearness")
        nearEntry = ttk.Entry(self, width=10)
        ## Pack widgets
        pathLabel.grid(row=1, column=1, padx=5, pady=15,
                       columnspan=2, sticky=tk.W)
        nearLabel.grid(row=2, column=1)
        nearEntry.grid(row=2, column=2)
        ## Set default values
        nearEntry.delete(0, tk.END)
        nearEntry.insert(0, disp(self.path.near))


class Interface(ttk.Frame):
    """Subclassed interface to the rest of the program."""
    def __init__(self, parent):
        ## Set the GUI state
        self.filename = None
        self.directory = None
        ## Set up links to persistent processing classes
        self.segment = segment.create_segment_object()
        self.contour = contour.create_contour_object()
        self.path = path.create_path_object()
        ## Start the actual interface
        ttk.Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()   #start it up
        
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
        self.segment_f = SegmentFrame(self.parent, self.segment)
        self.segment_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                            fill=tk.BOTH, ipadx=10, ipady=10)
        self.contour_f = ContourFrame(self.parent, self.contour)
        self.contour_f.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES,
                            fill=tk.BOTH, ipadx=10, ipady=10)
        self.path_f = PathFrame(self.parent, self.path)
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
