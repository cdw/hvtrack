#!/usr/bin/env python
# encoding: utf-8
""" segment.py
Created by Dave Williams on 2013.11.12

segment.py distinguishes trackable moving objects from the background to
tracks them over time.
"""

import numpy as np
import cv2

def create_segment_object()
    """Create a segmentation object with default parameters."""
    return Segment()

class Segment(object):
    """Detect foreground objects, generate tracks of them over time.
    The basic order:
        - perform a threshold on the background subtracted image
        - erode and dilate the image to remove smaller speckles
        - provide a resulting final binary image
    """
    def __init__(self, min_thresh=10, thresh_area=101,
                 open_kernel_x=10, open_kernel_y=10):
        """Initialize the values we will use during segmentation.

        Takes:
            min_thresh - the minimum threshold value to count as foreground
            thresh_area - the area to consider when adaptively thresholding
            open_kernel_x - the x scale of object to select for in opening
            open_kernel_y - the y scale of object to select for in opening
        Gives:
            None
        """
        self.min_thresh = min_thresh
        self.thresh_area = thresh_area
        self.open_kernel_x = open_kernel_x
        self.open_kernel_y = open_kernel_y
    
    def set_min_thresh(self, min_thresh):
        """Set the minimum threshold for non-adaptive thresholding."""
        self.thresh_area = thresh_area

    def set_thresh_area(self, thresh_area):
        """Set the adaptive threshold area"""
        self.thresh_area = thresh_area

    def set_open_kernal(self, open_kernel_x, open_kernel_y):
        """Set the morphological opening kernel x and y dimensions."""
        self.open_kernel_x = open_kernel_x
        self.open_kernel_y = open_kernel_y

    def abs_thresh(self, img, min_thresh=self.min_thresh, invert=False):
        """Perform an absolute threshold on the passed image.
        
        More documentation on the absolute threshold and its arguments is
        located here: http://tinyurl.com/knwcta4
        Takes:
            img - the image to threshold
            min_thresh - the minimum intensity of the threshold
            invert - if True, then areas above the threshold are set to zero
                     and areas below it are set to the max value (False)
        Gives:
            img - the thresholded image
        """
        if invert:
            thresh_type = cv2.cv.CV_THRESH_BINARY_INV 
        else:
            thresh_type = cv2.cv.CV_THRESH_BINARY
        img = cv2.threshold(
                np.uint8(img.round()), # must convert to uint8
                min_thresh,            # threshold value
                255,                   # value to assign to matched pix
                thresh_type)[1]        # inverted or not, return only the image
        return img

    def thresh(self, img, area=self.thresh_area):
        """Perform an adaptive threshold on the passed image.
        
        Documentation on the adaptive threshold and its arguments is located
        here: http://tinyurl.com/nughkox
        Takes: 
            img - the image to threshold
            area - pixel area to average over for determining the threshold
        Gives:
            img - the thresholded image
        """
        adaptiveMethod = cv2.cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C 
        thresholdType = cv2.cv.CV_THRESH_BINARY
        img = cv2.adaptiveThreshold(
                    np.uint8(img.round()), # must convert to uint8
                    255,                   # value to assign to matched pix
                    adaptiveMethod,        # Gaussian or mean
                    thresholdType,         # binary or binary inverted
                    self.thresh_area,      # area to consider
                    0)                     # blocksize
        return img

    def open(self, img, ok_x=self.open_kernel_x, ok_y=self.open_kernel_y):
        """Perform a morphological open on the passed image.
        
        This uses the predefined opening kernels to reduce speckle. 
        A nice explanation of openings is here: http://tinyurl.com/np9nv5e
        Takes:
            img - the image to open
            ok_x - the x distance to open over
            ok_y - the y distance to open over
        Gives:
            img - the opened image
        """
        k =  np.ones((ok_y, ok_x))
        return cv2.dilate(cv2.erode(img, k),k)
