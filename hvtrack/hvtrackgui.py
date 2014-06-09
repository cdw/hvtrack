#!/usr/bin/env python
# encoding: utf-8
"""
hvtrackgui.py - initial stab at tracker gui

Created by Dave Williams on 2014-04-21
"""

import Tkinter as tk
import ttk
import tkFileDialog
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
import os
# Local imports
import video
import background
import segment
import contour
import path


# Utility function
def disp(input_num_or_none):
    """Numbers returned as integer strings, Nones as blank strings."""
    if input_num_or_none is not None:
        return "%i"%input_num_or_none
    else:
        return ""

def bind_entry(widget, call):
    """Bind an entry widget to a call for focus loss or hitting return."""
    widget.bind('<Return>', call)
    widget.bind('<FocusOut>', call)
    return widget

def set_entry(widget, value):
    """Clear and set an entry widget."""
    widget.delete(0, tk.END)
    widget.insert(0, disp(value))


# Piecewise frames
class SegmentFrame(ttk.Frame):
    """Configure a segment instance."""
    def __init__(self, parent, segment):
        self.segment = segment  # A passed segment class instance
        ## GUI setup
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        segment_label = ttk.Label(self, text="Foreground segmentation")
        thresh_label = ttk.Label(self, text="Threshold Area")
        thresh_entry = ttk.Entry(self, width=7)
        open_x_label = ttk.Label(self, text="Opening X")
        open_x_entry = ttk.Entry(self, width=7)
        open_y_label = ttk.Label(self, text="Opening Y")
        open_y_entry = ttk.Entry(self, width=7)
        ## Pack widgets
        segment_label.grid(row=1, column=1, padx=5, pady=15,
                          columnspan=3, sticky=tk.W)
        thresh_label.grid(row=2, column=1, padx=5, pady=5)
        thresh_entry.grid(row=2, column=2, padx=5, pady=5)
        open_x_label.grid(row=2, column=3, padx=5, pady=5)
        open_x_entry.grid(row=2, column=4, padx=5, pady=5)
        open_y_label.grid(row=2, column=5, padx=5, pady=5)
        open_y_entry.grid(row=2, column=6, padx=5, pady=5)
        ## Set default values
        set_entry(thresh_entry, self.segment.thresh_area)
        set_entry(open_x_entry, self.segment.open_kernel_x)
        set_entry(open_y_entry, self.segment.open_kernel_y)
        ## Bind widgets
        self.thresh_entry = bind_entry(thresh_entry, self.thresh_call)
        self.open_x_entry = bind_entry(open_x_entry, self.open_x_call)
        self.open_y_entry = bind_entry(open_y_entry, self.open_y_call)

    # Set values function calls
    def thresh_call(self, *args):
        self.segment.set_thresh_area(self.thresh_entry.get())

    def open_x_call(self, *args):
        self.segment.set_open_kernal_x(self.open_x_entry.get())

    def open_y_call(self, *args):
        self.segment.set_open_kernal_y(self.open_y_entry.get())


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
        ## Set default values
        set_entry(area_min_entry, self.contour.area_min)
        set_entry(area_max_entry, self.contour.area_max)
        set_entry(perim_min_entry, self.contour.perim_min)
        set_entry(perim_max_entry, self.contour.perim_max)
        set_entry(ratio_min_entry, self.contour.ratio_min)
        set_entry(ratio_max_entry, self.contour.ratio_max)
        ## Bind widgets
        self.area_min_entry = bind_entry(area_min_entry, self.area_min_call)
        self.area_max_entry = bind_entry(area_max_entry, self.area_max_call)
        self.perim_min_entry = bind_entry(perim_min_entry, self.perim_min_call)
        self.perim_max_entry = bind_entry(perim_max_entry, self.perim_max_call)
        self.ratio_min_entry = bind_entry(ratio_min_entry, self.ratio_min_call)
        self.ratio_max_entry = bind_entry(ratio_max_entry, self.ratio_max_call)

    # Set values function calls
    def area_min_call(self, *args):
        self.contour.set_contour_area_min(self.area_min_entry.get())

    def area_max_call(self, *args):
        self.contour.set_contour_area_max(self.area_max_entry.get())

    def perim_min_call(self, *args):
        self.contour.set_contour_perim_min(self.perim_min_entry.get())

    def perim_max_call(self, *args):
        self.contour.set_contour_perim_max(self.perim_max_entry.get())

    def ratio_min_call(self, *args):
        self.contour.set_contour_ratio_min(self.ratio_min_entry.get())

    def ratio_max_call(self, *args):
        self.contour.set_contour_ratio_max(self.ratio_max_entry.get())


class PathFrame(ttk.Frame):
    """Configure a path instance."""
    def __init__(self, parent, path):
        self.path = path  # A passed path class instance
        ## GUI setup
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        path_label = ttk.Label(self, text="Path matching")
        near_label = ttk.Label(self, text="Nearness")
        near_entry = ttk.Entry(self, width=10)
        length_label = ttk.Label(self, text="Min length")
        length_entry = ttk.Entry(self, width=10)
        ## Pack widgets
        path_label.grid(row=1, column=1, padx=5, pady=15,
                       columnspan=2, sticky=tk.W)
        near_label.grid(row=2, column=1)
        near_entry.grid(row=2, column=2)
        length_label.grid(row=2, column=3)
        length_entry.grid(row=2, column=4)
        ## Set default values
        set_entry(near_entry, self.path.near)
        set_entry(length_entry, self.path.min_length)
        ## Bind widgets
        self.near_entry = bind_entry(near_entry, self.near_call)
        self.length_entry = bind_entry(length_entry, self.length_call)

    def near_call(self, *args):
        """Write the entry value to the path variable."""
        self.path.set_near(self.near_entry.get())

    def length_call(self, *args):
        """Write the entry value to the path variable."""
        self.path.set_min_length(self.length_entry.get())


class ImageFrame(ttk.Frame):
    """Display an image."""
    def __init__(self, parent, size=None):
        self.size = (600,480) if size is None else size
        self.contrast = 10
        ## GUI setup
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Put all the UI widgets where they go."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)
        ## Create widgets
        image_frame_label = ttk.Label(self, text="Video display")
        contrast_label = ttk.Label(self, text="Contrast enhancement")
        contrast_entry = ttk.Entry(self, width=10)
        photo = ImageTk.PhotoImage(Image.fromarray(np.zeros(self.size).T))
        image_label = ttk.Label(self)
        image_label.configure(image=photo)
        image_label.image = photo  # keep ref to prevent garbage collection
        ## Pack widgets
        image_frame_label.grid(row=1, column=1, padx=5, pady=5,
                               columnspan=3, sticky=tk.W)
        contrast_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.E)
        contrast_entry.grid(row=1, column=5, padx=5, pady=5, 
                            sticky=tk.E+tk.W)
        image_label.grid(row=2, column=1, padx=5, pady=5,
                         columnspan=5, sticky=tk.S)
        ## Set default values
        set_entry(contrast_entry, self.contrast)
        ## Bind widgets
        self.image_label = image_label
        self.contrast_entry = bind_entry(contrast_entry, self.contrast_call)

    def contrast_call(self, *args):
        """Write the entry value to the contrast variable."""
        self.contrast = self.contrast_entry.get()

    def update_image(self, image):
        """Update the displayed image with the passed image, scaled.

        The image will be rescaled to size before it is displayed. 
        Takes:
            image - an image of the video under examination
        Gives:
            None
        """
        pil_img = Image.fromarray(image).resize(self.size).convert("L")
        enhancer = ImageEnhance.Contrast(pil_img)
        tk_img = ImageTk.PhotoImage(enhancer.enhance(self.contrast))
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img  # prevent garbage collection
        self.update()  # allow the frame to complete its updates
        return


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
        self.image_f = ImageFrame(self.parent)
        self.image_f.pack(side=tk.RIGHT, expand=tk.YES,
                         fill=tk.BOTH, ipadx=10, ipady=10)
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
        quitButton.pack(side=tk.LEFT, padx=5, pady=5)
        #Video
        videoLabel = ttk.Label(self.video_f, text="Video")
        fileLabel = ttk.Label(self.video_f, text="File:")
        fileEntry = ttk.Entry(self.video_f, width=30)
        fileButton = ttk.Button(self.video_f, text="File", command=self.askOpen)
        dirLabel = ttk.Label(self.video_f, text="Directory:")
        dirEntry = ttk.Entry(self.video_f, width=30)
        dirButton = ttk.Button(self.video_f, text="Dir", command=self.askDir)
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
        self.run_file(fname)
        print fname
    
    def askDir(self):
        """Ask for a directory, then run the tracker on it"""
        dirname = tkFileDialog.askdirectory()
        hummertracker.dir_to_traces(dirname)
        print dirname

    def run_file(self, filename):
        """Take a passed filename, and get process it."""
        vid = video.open_video_file(filename)
        bkg = background.create_background_object(vid)
        # For testing
        self.image_f.update_image(bkg.subtract_background(100))
        print "updated?"
        # End for testing
        contour_log = []
        for img in bkg.subtracted_frames():
            #self.image_f.update_image(img)
            seg = self.segment.segment(img)
            con = self.contour.contour_and_filter(seg)
            self.image_f.update_image(self.contour.image_from_contours(
                                                        con, img.shape))
            contour_log.append(con)
            paths = self.path.contours_to_paths(contour_log)
        return paths


def main():
    root = tk.Tk()
    #root.geometry("350x100+300+300")
    app = Interface(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
