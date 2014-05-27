#!/usr/bin/env python
# encoding: utf-8
""" contour.py
Created by Dave Williams on 2013.11.12

contour.py takes a binary image, calculates and filters its contours.
"""

import cv2


def create_contour_object():
    """Create a contour object with default settings."""
    return Contour()


class Contour(object):
    """Using a binary image, select and filter objects.
    The basic order:
        - create contours from binary image
        - filter the contours by size and convexity
        - provide an array of contoured objects
    """
    def __init__(self, contour_area_min=10, contour_area_max=3000,
                 contour_perim_min=10, contour_perim_max=200,
                 contour_ratio_min=2, contour_ratio_max=500):
        """
        Remember the multitude of parameters needed to filter contours.
        Takes:
            contour_area_min - the minimum area enclosed by a valid contour
            contour_area_max - the maximum area enclosed by a valid contour
            contour_perim_min - the minimum perimeter of a valid contour
            contour_perim_max - the maximum perimeter of a valid contour
            contour_ratio_min - the minimum area/perimeter ratio
            contour_ratio_max - the maximum area/perimeter ratio
        """
        self.contour_area_min = contour_area_min
        self.contour_area_max = contour_area_max
        self.contour_perim_min = contour_perim_min
        self.contour_perim_max = contour_perim_max
        self.contour_ratio_min = contour_ratio_min
        self.contour_ratio_max = contour_ratio_max

    def set_contour_area_min(self, contour_area_min):
        """Change the minimum contour area of interest."""
        self.contour_area_min = contour_area_min

    def set_contour_area_max(self, contour_area_max):
        """Change the maximum contour area of interest."""
        self.contour_area_max = contour_area_max

    def set_contour_perim_min(self, contour_perim_min):
        """Change the minimum contour perimeter of interest."""
        self.contour_perim_min = contour_perim_min

    def set_contour_perim_max(self, contour_perim_max):
        """Change the maximum contour perimeter of interest."""
        self.contour_perim_max = contour_perim_max

    def set_contour_ratio_min(self, contour_ratio_min):
        """Change the minimum contour ratio of interest."""
        self.contour_ratio_min = contour_ratio_min

    def set_contour_ratio_max(self, contour_ratio_max):
        """Change the maximum contour ratio of interest."""
        self.contour_ratio_max = contour_ratio_max

    @staticmethod
    def contours_from_image(img):
        """Convert a binary image to a set of contours.

        Takes:
            img - a black and white binary image (foreground is white)
        Gives:
            contours - a list of contours
        """
        contours, hierarchy = cv2.findContours(img,
                                               cv2.RETR_CCOMP,
                                               cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def single_contour_center(contour):
        """Return the center of a single contour."""
        cm = cv2.moments(contour)
        center = (cm['m10']/cm['m00'], cm['m01']/cm['m00'])
        return center

    def _contour_centers(self, contours):
        """Return the centers of a list of contours."""
        return [self.single_contour_center(c) for c in contours]

    def _filter_contours(self, contours):
        """Filter contours by area and perimeter sizes."""
        out = []
        for contour in contours:
            area = cv2.contourArea(contour)
            perim = cv2.arcLength(contour, True)
            ratio = area/(perim+0.01)  # 0.01 to prevent division by zero
            if all((area > self.contour_area_min,
                    area < self.contour_area_max,
                    perim > self.contour_perim_min,
                    perim < self.contour_perim_max,
                    ratio > self.contour_ratio_min,
                    ratio < self.contour_ratio_max)):
                out.append(contour)
        return out

    def contour_and_filter(self, img):
        """Contour and filter a binary image, returning a list of contours."""
        return self._filter_contours(self.contours_from_image(img))

    def filtered_contour_centers(self, img):
        """Gives a list of contour centers that match current criteria."""
        return self._contour_centers(self.contour_and_filter(img))

    def unfiltered_contour_centers(self, img):
        """Gives a list of contour centers, without filtering."""
        return self._contour_centers(self.contours_from_image(img))
