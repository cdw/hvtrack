#!/usr/bin/env python
# encoding: utf-8
""" Video.py
Created by Dave Williams on 2013.11.07

Video.py contains the class which handles the loading and access to video files
for the tracker. It provides a uniform interface which abstracts away the
details of which video file type you are dealing with.
"""

try:
    import cv2
    import tiffcapture as tc
except ImportError, e:
    raise Exception("You'll need both OpenCV and TiffCapture installed. OpenCV can be gotten with 'brew install opencv' on a Mac or from opencv.org on Windows and TiffCapture can be gotten with 'pip install tiffcapture' on any platform.")


class Video(object):
    """An access class for reading video frames"""
    def __init__(self, filename=None):
        """Prepare yourself"""
        self._is_open = False  # Set true on opening
        self.open(filename)
    
    def __iter__(self):
        return self
    
    def _to_grayscale(self, img):
        """It is a whole lot easier to deal with grayscale, so convert"""
        if len(img.shape) > 1:
            img = img.mean(-1)
        return img
    
    def open(self, filename):
        """Open the video file and attach it to the class.
        Takes:
            filename - the full path to the video
        Gives:
            isOpened - True if opened, False otherwise
        """
        if filename is not None:
            self.filename = filename
            ext = filename.split('.')[-1]
            if ext in ['tiff', 'tif', 'TIF', 'TIFF']:
                # For tiffs use tiffcapture
                self.format = 'TIFF'
                self.video = tc.opentiff(filename)
                self._is_open = True
                self.length = self.video.length
                self.shape = self.video.shape
                self._curr = 0
            else:
                # For other formats try opencv
                self.format = 'CV'
                self.video = cv2.VideoCapture(filename)
                self._is_open = True
                self.length = self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
                self.shape = (
                    int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                    int(self.video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
                self._curr = 0
        return self.isOpened()
    
    def next(self):
        """Grab and read the next frame, stopping iteration at file end.
        This retrofit allows us to iterate over the files, even though OpenCV
        doesn't support it."""
        if self._is_open and self.format=='TIFF':
            return self._to_grayscale(self.video.next())
        elif self._is_open and self.format=='CV':
            if self.video.grab() is True:
                return self._to_grayscale(self.retrieve()[1])
            else:
                raise StopIteration()
        else:
            raise StopIteration()
        return
    
    def find_and_read(self, i):
        """Find and return a specific frame number, i."""
        if self.format=='TIFF':
            return self._to_grayscale(self.video.find_and_read(i))
        else:
            self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
            return self._to_grayscale(self.video.retrieve()[1])
        return
    
    def seek(self, i):
        """Set a given frame as the current."""
        if self.format=='TIFF':
            self.video.seek()
        else:
            self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
        return
    
    def release(self):
        """Release the open file by severing the connection to the video."""
        if self.isOpened() is True:
            del(self.video)
            self._is_open = False
        return
    


## The following are legacy code, to be shunted into other bits of the project
## at a future date

def play_video(cvtiff, framerate=12, size=(800,600)):
    """Playback an array stack of cv2 images/numpy arrays
    Takes:
        cvtiff: the array of numpy arrays
        framerate: fps (12)
        size: window size, None means don't resize ((800,600))
    """
    cv2.namedWindow('video')
    for img in cvtiff:
        if size is not None:
            img = cv2.resize(img, size)
        else:
            pass
        cv2.imshow('video', img)
        cv2.waitKey(1000/framerate)
    cv2.destroyWindow('video')

def write_video(imgstack, filename = '/Users/dave/Desktop/videoout.avi',
               size = (800, 600), tc=False):
    """Write out a video, starting from an array of numpy arrays"""
    # Must be 3 deep...
    if tc is False and len(imgstack[0].shape) == 2:
        imgstack = [np.tile(i, (3,1,1)) for i in imgstack]
    fps = 12.0
    fourcc = cv2.cv.FOURCC('I', 'Y', 'U', 'V') 
    # size = (imgstack[0].shape[1], imgstack[0].shape[0]) 
    writer = cv2.VideoWriter(filename, fourcc, fps, size)
    if tc is True:
        imgstack.seek(0)
        for i in range(imgstack.length):
            frame = cv2.resize(imgstack.read()[1][1], size)
            writer.write(frame)
        writer.release()
    else:
        for frame in imgstack:
            frame = cv2.resize(frame, size)
            writer.write(frame)
        writer.release()

def mog_background_subtract(cvtiff):
    #BackgroundSubtractorMOG(history, nmixtures, backgroundRatio[, noiseSigma])
    bgs = cv2.BackgroundSubtractorMOG(48, 5, 0.1, 0.1)
    cv2.namedWindow("input")
    for img in cvtiff:
        fgmask = bgs.apply(img)
        fgmask = cv2.resize(fgmask, (800, 600))
        cv2.imshow("input", fgmask)
        cv2.waitKey(10)
    cv2.destroyWindow("input")
    return cvtiff

