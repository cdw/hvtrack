#!/usr/bin/env python
# encoding: utf-8
""" path.py
Created by Dave Williams on 2013.11.14

path.py matches contour center points tracked over multiple frames to a single
object, creating its path.
"""

import cv2
import numpy as np


def create_path_object():
    """Create a path object with default parameters."""
    return Path()


class Path(object):
    """Match contour center points over frames, making a path.
    The basic order:
        - check if new points are near ends of existing paths, add to path if
          such exists
        - check if new points are near predicted next location of existing
          paths, add to path if such exists (TODO)
        - if additional new points remain, form a new path for each
        - prune paths which have not had a new point added
        - produce a list of paths for the contour sequence
    Contours fed in should be a list of contours at each time point (frame)
    Each path produced is in the format [[frame num, contour], [frame num,
    contour], ... ]
    """
    def __init__(self, near=None, min_length=None):
        """Initialize the values needed for path tracking.

        Takes:
            near - the pixel distance below which a point is considered near
                   the end of a track
            min_length - the minimum number of frames across which a path must
                         stretch to be counted
        Gives:
            None
        """
        # Default values
        self.near_default = 100
        self.min_length_default = 3
        default_if_none = lambda val, de: de if val is None else val
        self.near = default_if_none(near, self.near_default)
        self.min_length = default_if_none(min_length, self.min_length_default)
        # Initialize path storages
        self.paths = []
        self.dead_paths = []

    def set_near(self, near):
        """Set how close a point has to be to count as near a track end."""
        if type(near) is str:
            if near == "":
                self.near = None
            else:
                self.near = int(round(float(near)))
        elif near is None:
            self.near = None

    def forget_paths(self):
        """Forget current traces to prepare for a new video."""
        self.paths = []
        self.dead_paths = []

    @staticmethod
    def _center(contour):
        """Return the center of a single contour."""
        cm = cv2.moments(contour)
        if cm['m00'] == 0 or cm['m00'] == 0:  # occurs with tiny contours
            return contour.mean(0)
        center = (cm['m10']/cm['m00'], cm['m01']/cm['m00'])
        return center

    def _nearby(self, path, contour):
        """True if a contour is nearby the end point of a current path.

        Takes:
            path - a path to check the last point of for nearness
            contour - the contour to check against the path
        Gives:
            close - True if the contour is closer to the last point than
                    self.near, False otherwise
        """
        c_cent = self._center(contour)
        p_cent = self._center(path[-1][1])
        distance = np.hypot(c_cent[0]-p_cent[0], c_cent[1]-p_cent[1])
        close = distance < self.near
        if close:
            return True
        else:
            return False

    def _sacrifice_dead_paths(self, time):
        """Kill off the old ones, paths for the path god.

        Remove any paths which haven't found a match in the current (passed)
        time step to the dead paths list.
        Takes:
            time - the current time, whose paths we are going to prune away
        Gives:
            None
        """
        for i in range(len(self.paths)):
            path = self.paths.pop(0)
            if path[-1][0]+1 < time:
                self.dead_paths.append(path)
            else:
                self.paths.append(path)
        return

    def _find_a_contour_a_home(self, contour, time):
        """Contours gotta live somewhere: in an existing path or in a new one.

        Check if a contour is a good fit to be appended to the ends of any of
        the existing paths. If it is, append it, if it isn't create a new path
        for it to sit in.

        Note: We're deliberately not checking to see if a path has already had
        something appended to it this time step. This means that if a speckle
        appears near the tracked object, we'll have two entries for a single
        frame, but this seems a better option than having the track forked to
        whichever speck comes first in the contour list.
        Takes:
            contour - the contour for which we wish to find a home
            time - the current frame number
        Gives:
            None
        """
        for i in range(len(self.paths)):
            path = self.paths.pop(0)
            if self._nearby(path, contour):
                path.append([time, contour])
                self.paths.append(path)
                break
            else:
                self.paths.append(path)
        else:
            self.paths.append([[time, contour]])
        return

    def path_meets_filters(self, path):
        """Check that a path meets the filter requirements.

        If a requirement value is None, it is not applied.
        """
        return len(path) >= self.min_length

    def contours_to_paths(self, contour_log):
        """Parse a contour log into paths.

        Convert contour logs, which is a list (by frame number) of lists (each
        contour found in that frame) into a list of paths. Each path is a list
        of contours and frame numbers thus: [[frame num, contour],
        [frame num, contour], ... ]
        Takes:
            contour_log: list of contours by frame number
        Give:
            dead_paths: a list of all the completed paths
        """
        for time in range(len(contour_log)):
            current_contours = contour_log[time]
            self._sacrifice_dead_paths(time)
            for contour in current_contours:
                self._find_a_contour_a_home(contour, time)
        for path in self.paths:
            self.dead_paths.append(path)
        self.dead_paths = filter(self.path_meets_filters, self.dead_paths)
        return self.dead_paths

    def save_path_centers(self, filename, path):
        """Write a path out as an array of frame numbers and center points.

        The output file takes the form of an array where each line is
        formatted: [frame number, contour_center_x, contour_center_y]
        Takes:
            filename - the output filename
            path - the path to save
        Gives:
            None
        """
        time_and_center = lambda c: (c[0], self._center(c[1])[0],
                                     self._center(c[1])[1])
        centers = np.array([time_and_center(c) for c in path])
        np.savetxt(filename, centers, '%.8e', ',')
