#!/usr/bin/env python
# encoding: utf-8
""" segment.py
Created by Dave Williams on 2013.11.12

segment.py distinguishes trackable moving objects from the background to
tracks them over time.
"""

import numpy as np
import cv2


def create_segment_object():
    """Create a segmentation object with default parameters."""
    return Segment()


class Segment(object):
    """Detect foreground objects, generate tracks of them over time.
    The basic order:
        - perform a threshold on the background subtracted image
        - erode and dilate the image to remove smaller speckles
        - provide a resulting final binary image
    """
    def __init__(self, min_thresh=None, thresh_area=None,
                 open_x=None, open_y=None):
        """Initialize the values we will use during segmentation.

        Takes:
            min_thresh - the minimum threshold value to count as foreground
            thresh_area - the area to consider when adaptively thresholding
            open_x - the x scale of object to select for in opening, in pix
            open_y - the y scale of object to select for in opening, in pix
        Gives:
            None
        """
        # Default values
        self._min_t_default = 10
        self._t_area_default = 101
        self._open_x_default = 10
        self._open_y_default = 10
        # Set current values from passed values
        default_if_none = lambda val, de: de if val is None else val
        self.min_thresh = default_if_none(min_thresh, self._min_t_default)
        self.thresh_area = default_if_none(thresh_area, self._t_area_default)
        self.open_kernel_x = default_if_none(open_x, self._open_x_default)
        self.open_kernel_y = default_if_none(open_y, self._open_y_default)

    @staticmethod
    def _passed_to_int(passed):
        """Convert passed (probably string) value for setting a local int."""
        if type(passed) is str:
            if passed == "":
                return None
            else:
                return int(round(float(passed)))
        elif passed is None:
            return passed
        elif type(passed) is float:
            return int(round(passed))
        elif type(passed) is int:
            return passed

    def set_min_thresh(self, min_thresh):
        """Set the minimum threshold for non-adaptive thresholding."""
        self.thresh_area = self._passed_to_int(min_thresh)

    def set_thresh_area(self, thresh_area):
        """Set the adaptive threshold area."""
        self.thresh_area = self._passed_to_int(thresh_area)

    def set_open_kernal_x(self, open_kernel_x):
        """Set the morphological opening kernel x dimension."""
        self.open_kernel_x = self._passed_to_int(open_kernel_x)

    def set_open_kernal_y(self, open_kernel_y):
        """Set the morphological opening kernel y dimension."""
        self.open_kernel_y = self._passed_to_int(open_kernel_y)

    def abs_thresh(self, img, min_thresh=None, invert=False):
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
        if min_thresh is None:
            min_thresh = self.min_thresh
        if invert:
            thresh_type = cv2.cv.CV_THRESH_BINARY_INV
        else:
            thresh_type = cv2.cv.CV_THRESH_BINARY
        img = cv2.threshold(
            np.uint8(img.round()),  # must convert to uint8
            min_thresh,             # threshold value
            255,                    # value to assign to matched pix
            thresh_type)[1]         # inverted or not, return only the image
        return img

    def thresh(self, img, area=None, invert=False):
        """Perform an adaptive threshold on the passed image.

        Documentation on the adaptive threshold and its arguments is located
        here: http://tinyurl.com/nughkox
        Takes:
            img - the image to threshold
            area - pixel area to average over for determining the threshold
            invert - if True, then areas above the threshold are set to zero
                     and areas below it are set to the max value (False)
        Gives:
            img - the thresholded image
        """
        if area is None:
            area = self.thresh_area
        adaptive_method = cv2.cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C
        if invert:
            threshold_type = cv2.cv.CV_THRESH_BINARY_INV
        else:
            threshold_type = cv2.cv.CV_THRESH_BINARY
        img = cv2.adaptiveThreshold(
            np.uint8(img.round()),  # must convert to uint8
            255,                    # value to assign to matched pix
            adaptive_method,        # Gaussian or mean
            threshold_type,         # binary or binary inverted
            self.thresh_area,       # area to consider
            0)                      # blocksize
        return img

    def open(self, img, ok_x=None, ok_y=None):
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
        if ok_x is None:
            ok_x = self.open_kernel_x
        if ok_y is None:
            ok_y = self.open_kernel_y
        k = np.ones((ok_y, ok_x))
        return cv2.dilate(cv2.erode(img, k), k)

    def segment(self, img):
        """Perform the default segmentation (threshold then open).

        Using the passed image and the current values for threshold area and
        opening kernel, perform a segmentation.
        Takes:
            img - the image to segment
        Gives:
            seg_img - the segmented image
        """
        return self.open(self.thresh(img))
