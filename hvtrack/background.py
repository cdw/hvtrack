#!/usr/bin/env python
# encoding: utf-8
""" background.py
Created by Dave Williams on 2013.11.07

background.py provides access to background subtraction mechanisms and their
associated parameters.
"""

import copy
import numpy as np


def create_background_object(video_object):
    """Create a background subtraction object from a passed video object."""
    return Background(video_object)


class Background(object):
    """Remember the background model for a video file."""
    def __init__(self, vid):
        """Get goin'."""
        self.video = copy.copy(vid)  # So current frame changes won't propagate
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
        # frame_mean = np.uint8(np.round(np.array(frames).mean(0)))
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

    def subtract_background(self, frame_ind, absolute=True):
        """Return a non-thresholded background-subtracted version of frame i.

        Note that the returned frame will not necessarily be in a format
        amenable to OpenCV usage, as it will be a numpy array of floats rather
        than 8 bit unsigned integers.

        Takes:
            frame_ind - frame number for which to find subtracted version
            absolute - whether to return the absolute value of the foreground,
                       a value of False will allow negative values (True)
        Gives:
            frame - the background subtracted frame
        """
        frame = np.subtract(self.video.find_and_read(frame_ind),
                            self.background_image(frame_ind))
        if absolute:
            frame = np.abs(frame)
        return frame

    def subtracted_frames(self):
        """Create a generator of background subtracted frames."""
        frame_number = 0
        video_length = int(self.video.length)
        while frame_number < video_length:
            yield self.subtract_background(frame_number)
            frame_number += 1
