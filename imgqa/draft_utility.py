# -*- coding: utf-8 -*-
"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
# import os
# import sys
# import unittest
# import collections
# import pandas as pd
import unittest
import cv2
from skimage.measure import compare_ssim as ssim
import numpy as np
import json
from simplejson import JSONDecodeError
import logging
import pandas as pd


class CompareFiles(unittest.TestCase):
    """File Comparison module which includes image, csv and workbook."""

    def compare_images(self, source_img, target_img):
        """Compare two images on the basis mse and ssim index.

        :param source_img: source image.
        :param target_img: target image.
        :return: list of boolean value of image comparision,
        mse value and ssim value.
        """
        # list of expected image extensions
        extn = ('jpg', 'jpeg', "png")
        if source_img.split(".") not in extn and\
                target_img.split(".") not in extn:
            logging.warning("Invalid image file extension")
            return False

        source = cv2.imread(source_img)
        target = cv2.imread(target_img)
        if self.__compare_images_structure(source, target) \
            and self.__compare_image_mse(source, target) \
                and self.__compare_image_ssim(source, target):
            logging.info("The images are perfectly similar")
            return True
        else:
            logging.warning("The images are not similar")
            self.__images_visual_difference(source, target)
            return False

    def __compare_images_structure(self, source_image, target_image):
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
                logging.warning("RGB Attributes are different\
                though images are same size")
                return False
        else:
            logging.warning("The images have different size and channels")
            return False

    def __compare_images_mse(self, source_image, target_image):
        """Checkpoint to measure Mean Square Error (MSE) difference of images.

        :param source_image:
        :param target_image:
        :return: returns boolean value based on images mse values
        :rtype: boolean value

        """
        mse_val = np.sum((source_image.astype("float") - target_image.astype("float")) ** 2)
        mse_val /= float(source_image.shape[0] * source_image.shape[1])

        if mse_val == 0.00:
            logging.info("Source and target images MSE Value are same")
            return True
        else:
            logging.warning("Source and target images\
            MSE Value: {0}" % mse_val)
            return False

    def __compare_images_ssim(self, source_image, target_image):
        """Checkpoint to measure Structural Similarity Index (SSIM) difference of images.

        :param source_image:
        :param target_image:
        :return: returns boolean value based on images ssim values
        :rtype: boolean value
        """
        ssim_val = ssim(source_image, target_image)
        if ssim_val == 1.00:
            logging.info("Source and target images SSIM Value sre same:")
            return True
        else:
            logging.warning("Source and target images\
            SSIM Value: {0}" % ssim_val)
            return ssim_val

    def __images_visual_difference(self, source_image, target_image):
        """"Show the images visual difference.

        :param source_image:
        :param target_image:
        :return: NA
        :rtype: NA
        """
        difference = cv2.subtract(source_image, target_image)
        cv2.imshow("difference", difference)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def compare_json(self, source, target):
        """Compare json files and returns text file with the difference.

        :param source: source json file Path.
        :param target: target json path.
        :return: True/False.
        :rtype: boolean
        """
        try:
            if source.split(".")[1] != 'json' and\
                    target.split(".")[1] != 'json':
                logging.warning("File extensions are not valid.")
                return False
            else:
                with open(source) as json1_dict:
                    source_dict = json.load(json1_dict)
                with open(target) as json2_dict:
                    target_dict = json.load(json2_dict)
            self.__compare_dictionaries(source_dict, target_dict, "json1_dict", "json2_dict")

        except JSONDecodeError:
            logging.warning("Invalid json.")

    def __compare_dictionaries(self, source, target, source_name, target_name, path=""):
        """Compare two dictionaries recursively to find non matching elements.

        Args:
            :param source: source dictionary
            :param target: target dictionary
            :param source_name: source dictionary name
            :param target_name: target dictionary name

        return:
        """
        err = ''
        key_err = ''
        value_err = ''
        old_path = path
        for k in source:
            path = old_path + "[%s]" % k
            if k not in target.keys():
                key_err += "Key %s%s not in %s\n" % (source_name, path, target_name)
            else:
                if isinstance(source[k], dict) and isinstance(target[k], dict):
                    err += self.__compare_dictionaries(source[k], target[k], 'd1', 'd2', path)
                else:
                    if source[k] != target[k]:
                        value_err += "Value of %s%s (%s) not same as %s%s (%s)\n"\
                            % (source_name, path, source[k], target_name, path, target[k])

        for k in target:
            path = old_path + "[%s]" % k
            if k not in source.keys():
                key_err += "Key %s%s not in %s\n" % (target_name, path, source_name)

        return key_err + value_err + err

    def compare_spreadsheet(self, source, target):
        """Compare two spreadsheets and generates an excel file containing the.

        difference. If resultant excel file contain empty cell that means
        the value is same in both excels else not.
        :param source: Source file Path.
        :param target: Target file path.
        :return: data that differs in source and target files.
        :rtype: data frame
        """
        file_extn = ('xls', 'xlsx', 'csv', 'tsv', 'hdf', 'html')
        if (source.split(".")[1] and target.split(".")[1]) in file_extn:
            source_data = self.__load_into_dataframe(source)
            target_data = self.__load_into_dataframe(target)
            if source_data.split('.')[1] and target_data.split('.')[1] in ('xls','xlsx'):
                # Validate length of work sheets
                # For every work sheet, iterate through the data
                # pd.ExcelFile().sheet_names
                pass

        else:
            logging.warning("File extensions are not valid.")
            return False

        return source_data[source_data != target_data]

    def __load_into_dataframe(self, source):
        if source.split(".")[1] in ('xls', 'xlsx'):
            return self.__read_speadsheet(source)
        elif source.split(".")[1] == 'csv':
            return self.__read_csv(source)
        elif source.split(".")[1] == 'hdf':
            return self.__read_hdf(source)
        elif source.split(".")[1] == 'html':
            return self.__read_html(source)
        elif source.split(".")[1] == 'tsv':
            return self.__read_tsv(source)

    def __read_speadsheet(self, sheet):
        return pd.read_excel(sheet)

    def __read_csv(self, csv, sep=None):
        return pd.read_csv(csv)

    def __read_hdf(self, hdf):
        return pd.read_hdf(hdf)

    def __read_html(self, html):
        return pd.read_html(html)

    def __read_tsv(self, tsv, sep='\t'):
        return pd.read_csv(tsv, sep=sep)

