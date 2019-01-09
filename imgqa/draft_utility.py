# -*- coding: utf-8 -*-
"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
import os
import sys
import unittest
import collections
import pandas as pd
import cv2
from skimage.measure import compare_ssim as ssim
import numpy as np
import json
from simplejson import JSONDecodeError
from matplotlib import pyplot as plt
import logging


class CompareFiles(unittest.TestCase):
    """File Comparison module which includes image, csv and workbook."""

    def __compare_image_structure(self, source_image, target_image):
        """Checkpoint 1 to measure on size and shape of image.

        :param source_image: source image
        :param target_image: target image
        :return: returns boolean value based on images structure similarity
        :rtype: boolean value.
        """
        if source_image.shape == target_image.shape:
            logging.info("Images of same size")
            difference = cv2.subtract(source_image, target_image)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == cv2.countNonZero(g) == cv2.countNonZero(r) == 0:
                logging.info("The images are completely Equal")
                return True
            else:
                logging.warning("RGB Attributes are different though images are same size")
                return False
        else:
            logging.warning("The images have different size and channels")
            return False

    def __compare_images_mse(self, source_image, target_image):
        """Checkpoint to measure on size and shape of image.

        :param source_image:
        :param target_image:
        :return: returns boolean value based on images mse values
        :rtype: boolean value

        """
        mse_val = np.sum((source_image.astype("float") - target_image.astype("float")) ** 2)
        mse_val /= float(source_image.shape[0] * source_image.shape[1])

        if mse_val == 0.00:
            return True
        elif mse_val > 0:
            logging.warning("Images MSE value: %s" % mse_val)
            return False

    def __compare_images_ssim(self, source_image, target_image):
        pass

    def compare_images(self, source_img, target_img):
        """Compare two images on the basis mse and ssim index.

        :param source_img: source image.
        :param target_img: target image.
        :return: list of boolean value of image comparision,
        mse value and ssim value.
        """
        # list of expected image extensions
        extn = ('jpg', 'jpeg', "png")
        if source_img.split(".") not in extn and target_img.split(".") not in extn:
            logging.error("Invalid image file extention")
            return False

        source = cv2.imread(source_img)
        target = cv2.imread(target_img)
        if self.__compare_image_structure(source, target) \
            and self.__compare_image_mse(source, target) \
            and self.__compare_image_ssim(source, target):
            logging.info("The images are perfectly similar")
            return True
        else:
            logging.warning("The images are not similar")

