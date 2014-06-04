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
    def __init__(self, area_min=None, area_max=None,
                 perim_min=None, perim_max=None,
                 ratio_min=None, ratio_max=None):
        """
        Remember the multitude of parameters needed to filter contours.
        Takes:
            area_min - minimum area enclosed by a valid contour
            area_max - maximum area enclosed by a valid contour
            perim_min - minimum perimeter of a valid contour
            perim_max - maximum perimeter of a valid contour
            ratio_min - minimum area/perimeter ratio
            ratio_max - maximum area/perimeter ratio
        """
        # Default values
        self._area_min_default = 10
        self._area_max_default = 3000
        self._perim_min_default = 10
        self._perim_max_default = 400
        self._ratio_min_default = None
        self._ratio_max_default = None
        # Current values from passed
        default_if_none = lambda val, de: de if val is None else val
        self.area_min = default_if_none(area_min, self._area_min_default)
        self.area_max = default_if_none(area_max, self._area_max_default)
        self.perim_min = default_if_none(perim_min, self._perim_min_default)
        self.perim_max = default_if_none(perim_max, self._perim_max_default)
        self.ratio_min = default_if_none(ratio_min, self._ratio_min_default)
        self.ratio_max = default_if_none(ratio_max, self._ratio_max_default)

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

    def set_contour_area_min(self, a_min):
        """Change the minimum contour area of interest."""
        self.area_min = self._passed_to_int(a_min, self._area_min_default)

    def set_contour_area_max(self, a_max):
        """Change the maximum contour area of interest."""
        self.area_max = self._passed_to_int(a_max, self._area_max_default)

    def set_contour_perim_min(self, p_min):
        """Change the minimum contour perimeter of interest."""
        self.perim_min = self._passed_to_int(p_min, self._perim_min_default)

    def set_contour_perim_max(self, p_max):
        """Change the maximum contour perimeter of interest."""
        self.perim_max = self._passed_to_int(p_max, self._perim_max_default)

    def set_contour_ratio_min(self, r_min):
        """Change the minimum contour ratio of interest."""
        self.ratio_min = self._passed_to_int(r_min, self._ratio_min_default)

    def set_contour_ratio_max(self, r_max):
        """Change the maximum contour ratio of interest."""
        self.ratio_max = self._passed_to_int(r_max, self._ratio_max_default)

    def print_filter_criteria(self):
        """Print and return as a dict the filter criteria."""
        criteria = {
            "Area min": self.area_min,
            "Area max": self.area_max,
            "Perimeter min": self.perim_min,
            "Perimeter max": self.perim_max,
            "Ratio min": self.ratio_min,
            "Ratio max": self.ratio_max}
        print(criteria)
        return criteria

    @staticmethod
    def contours_from_image(img):
        """Convert a binary image to a set of contours.

        Takes:
            img - a black and white binary image (foreground is white)
        Gives:
            contours - a list of contours
        """
        contours, _ = cv2.findContours(img,
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

    def contour_meets_filters(self, contour):
        """Check that a contour meets the filter requirements.

        If a requirement value is None, it is not applied.
        """
        area = cv2.contourArea(contour)
        perim = cv2.arcLength(contour, True)
        ratio = area/(perim+0.01)  # 0.01 to prevent division by zero
        more_or_none = lambda val, base: any((val > base, base is None))
        less_or_none = lambda val, base: any((val < base, base is None))
        if any((not more_or_none(area, self.area_min),
                not less_or_none(area, self.area_max),
                not more_or_none(perim, self.perim_min),
                not less_or_none(perim, self.perim_max),
                not more_or_none(ratio, self.ratio_min),
                not less_or_none(ratio, self.ratio_max))):
            return False
        else:
            return True

    def _filter_contours(self, contours):
        """Filter contours by area and perimeter sizes."""
        return filter(self.contour_meets_filters, contours)

    def contour_and_filter(self, img):
        """Contour and filter a binary image, returning a list of contours."""
        return self._filter_contours(self.contours_from_image(img))

    def filtered_contour_centers(self, img):
        """Gives a list of contour centers that match current criteria."""
        return self._contour_centers(self.contour_and_filter(img))

    def unfiltered_contour_centers(self, img):
        """Gives a list of contour centers, without filtering."""
        return self._contour_centers(self.contours_from_image(img))
