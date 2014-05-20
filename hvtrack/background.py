#!/usr/bin/env python
# encoding: utf-8
""" Background.py
Created by Dave Williams on 2013.11.07

Background.py provides access to background subtraction mechanisms and their
associated parameters. 
"""

import copy
import numpy as np
import cv2

def create_background_object(video_object):
    """Create a background subtraction object from a passed video object."""
    return Background(video_object)

class Background(object):
    """Remember the background model for a video file."""
    def __init__(self, vid):
        """Get goin'."""
        self.video = copy.copy(vid) # So current frame changes won't propagate
        self._first_ten = self._naive_background()

    def _naive_background(self):
        """Find the mean of the first ten frames.
       
        Takes:
            Nothing
        Gives:
            frame_mean - the mean of the first ten frames
        """
        frames = [self.video.find_and_read(i) for i in range(10)]
        frame_mean = np.array(frames).mean(0)
        #frame_mean = np.uint8(np.round(np.array(frames).mean(0)))
        return frame_mean 

    def background_image(self, frame_ind=None):
        """Find the static background image to the passed video.
        
        We take the mean of the first ten frames to be the representative
        background image for any passed frame index, but this may later
        change to a more robust method.
        
        Takes: 
            frame_ind - frame number for which to find the background image
        Gives:
            background - the background image
        """
        return self._first_ten
    
    def subtract_background(self, frame_ind):
        """Return a non-thresholded background-subtracted version of frame i.
        
        Note that the returned frame will not necessarily be in a format 
        amenable to OpenCV usage, as it will be a numpy array of floats rather
        than 8 bit unsigned integers.

        Takes:
            frame_ind - frame number for which to find subtracted version
        Gives:
            frame - the background subtracted frame
        """
        frame = np.subtract(self.video.find_and_read(frame_ind), 
                            self.background_image(frame_ind))
        return frame
        
