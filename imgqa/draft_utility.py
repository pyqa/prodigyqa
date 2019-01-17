# -*- coding: utf-8 -*-
"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
import unittest
import cv2
from skimage.measure import compare_ssim as ssim
import numpy as np
import json
from simplejson import JSONDecodeError
import logging
import pandas as pd


class Compare(unittest.TestCase):
    """File Comparison module which includes image, csv and workbook."""

    def images(self, source, target):
        """Compare images on the basis mse and ssim index.

        :param source: source image path.
        :param target: target image path.
        :return: True/False.
        :rtype: bool.
        """
        image_extn = ('jpg', 'jpeg', "png")
        if source.split(".") and target.split(".") not in image_extn:
            logging.warning("Invalid image extension")
            return False

        source = cv2.imread(source)
        target = cv2.imread(target)
        if self.__compare_images_structure(source, target) \
            and self.__compare_image_mse(source, target) \
                and self.__compare_image_ssim(source, target):
            logging.info("The images are perfectly similar")
            return True
        else:
            logging.warning("The images are not similar")
            self.__images_visual_difference(source, target)
            return False

    def __compare_images_structure(self, source, target):
        """Checkpoint to measure on size and shape of image.

        :param source: source image path.
        :param target: target image path.
        :return: True/False.
        :rtype: bool.
        """
        if source.shape == target.shape:
            logging.info("Images of same size")
            difference = cv2.subtract(source, target)
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

    def __compare_images_mse(self, source, target):
        """Checkpoint to measure Mean Square Error (MSE) difference of images.

        :param source: Source image path.
        :param target: Target Image path.
        :return: True/False.
        :rtype: bool.

        """
        mse_val = np.sum((source.astype("float") - target.astype("float")) ** 2)
        mse_val /= float(source.shape[0] * source.shape[1])

        if mse_val == 0.00:
            logging.info("Source and target images have same MSE value")
            return True
        else:
            logging.warning("Source and target images have different MSE Value: {0}" % mse_val)
            return False

    def __compare_images_ssim(self, source, target):
        """Checkpoint to measure Structural Similarity Index (SSIM) difference of images.

        :param source: Source Image path.
        :param target: Target Image path.
        :return: True/False.
        :rtype: bool.
        """
        ssim_val = ssim(source, target)
        if ssim_val == 1.00:
            logging.info("Source and target images have same SSIM Value")
            return True
        else:
            logging.warning("Source and target images have different SSIM value: {0}" % ssim_val)
            return ssim_val

    def __images_visual_difference(self, source, target):
        """"Show the images visual difference.

        :param source: Source image path.
        :param target: Target image path.
        :return: NA
        :rtype: NA
        """
        difference = cv2.subtract(source, target)
        cv2.imshow("difference", difference)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def json(self, source, target):
        """Compare json files.

        :param source: source json file Path.
        :param target: target json path.
        :return: NA.
        :rtype: NA.
        """
        try:
            if source.split(".")[1] and target.split(".")[1] != 'json':
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

        :param source: source dictionary.
        :param target: target dictionary.
        :param source_name: source dictionary name.
        :param target_name: target dictionary name.
        :return: non matching elements of two dictionaries.
        :rtype: str.
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

    def files(self, source, target):
        """Compare two files of type xls or xlsx or html or hdf or csv or tsv and return difference and boolean.

        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        file_extn = ('xls', 'xlsx', 'csv', 'tsv', 'hdf', 'html')

        if (source.split(".")[1] and target.split(".")[1]) in file_extn:
            if (source.split(".")[1] and target.split(".")[1]) in ('xls', 'xlsx'):
                return self.__compare_workbooks(source, target)
            elif source.split(".")[1] in ('xls', 'xlsx') and target.split(".")[1] not in ('xls', 'xlsx'):
                return self.__compare_spreadsheet_and_non_spreadsheet(source, target)
                pass
            elif source.split(".")[1] not in ('xls', 'xlsx') and target.split(".")[1] in ('xls', 'xlsx'):
                return self.__compare_spreadsheet_and_non_spreadsheet(source, target)
                pass
            elif (source.split(".")[1] and target.split(".")[1]) not in ('xls', 'xlsx'):
                return self.__compare_non_workbook_files(source, target)
        else:
            logging.warning("File extensions are not valid.")
            return False

    def __compare_workbooks(self, source, target):
        """Compare two xls or xlsx files and return difference and boolean.

        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        source_dataframe = pd.ExcelFile(source)
        target_dataframe = pd.ExcelFile(target)
        flag = 0
        if source_dataframe.sheet_names == target_dataframe.sheet_names:
            source_sheets = source_dataframe.sheet_names
            for source_sheet in source_sheets:
                if source_dataframe.parse(source_sheet) == target_dataframe.parse(source_sheet):
                    logging.info("Spreadsheet '{0}' of " /
                                 "source '{1}' and target '{2}' have same data".format /
                                 (source_sheet, source.split(".")[0], target.split(".")[0]))
                else:
                    difference = source_dataframe.parse(source_sheet)[source_dataframe.parse(source_sheet) != target_dataframe.parse(source_sheet)]
                    logging.warning("Spreadsheet '{0}' of " /
                                    "source '{1}' and target '{2}' have different data\n {3}".format /
                                    (source_sheet, source.split(".")[0], target.split(".")[0], difference))
                    flag += 1
            if flag == 0:
                logging.info("Both source '{0}' and target '{1}' work" /
                             "books have same data".format(source_sheet, source.split(".")[0], target.split(".")[0]))
                return True
            else:
                logging.info("one or more spread sheets of source '{0}' and target '{1}'" /
                             "have different data".format(source_sheet, source.split(".")[0], target.split(".")[0]))
                return False

    def __compare_non_workbook_files(self, source, target):
        """Compare two html or hdf or csv or tsv and return difference and boolean.

        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        source_data = self.__load_into_dataframe(source)
        target_data = self.__load_into_dataframe(target)
        difference = source_data[source_data != target_data]
        if difference == '':
            logging.info("Both source '{0}' and target '{1}'" /
                         "have same data".format(source.split(".")[0], target.split(".")[0]))
            return True
        else:
            logging.warning("Source '{0}' and target '{1}'" /
                            "have different data\n {2}".format(source.split(".")[0], target.split(".")[0], difference))
            return False

    def __compare_spreadsheet_and_non_spreadsheet(self, source, target):
        """Compare two files of xls or xlsx and html or hdf or csv or tsv and return difference and boolean.

        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        if source.split(".")[1] in ('xls', 'xlsx') and target.split(".")[1] not in ('xls', 'xlsx'):
            df = pd.ExcelFile(source)
            data = self.__load_into_dataframe(target)
        elif source.split(".") not in ('xls', 'xlsx')[1] and target.split(".")[1] in ('xls', 'xlsx'):
            df = pd.ExcelFile(target)
            data = self.__load_into_dataframe(source)
        for sheet in df.sheet_names:
            if df.parse(sheet) in data:
                logging.info("Both source '{0}' and target '{1}'" /
                             "have same data".format(source.split(".")[0], target.split(".")[0]))
                break
        else:
            logging.warning("source '{0}' and target '{1}'" /
                            "have different data".format(source.split(".")[0], target.split(".")[0]))
            return False
        return True

    def __load_into_dataframe(self, source):
        """Load hdf or csv or tsv file and return data.

        :param source: source file path
        :return: file data.
        :rtype: data frame.
        """
        if source.split(".")[1] == 'csv':
            return self.__read_csv(source)
        elif source.split(".")[1] == 'hdf':
            return self.__read_hdf(source)
        elif source.split(".")[1] == 'html':
            return self.__read_html(source)
        elif source.split(".")[1] == 'tsv':
            return self.__read_tsv(source)

    def __read_csv(self, source, sep=None):
        """Load csv file and return data.

        :param source: source file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(source)

    def __read_hdf(self, source):
        """Load hdf file and return data.

        :param source: source file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_hdf(source)

    def __read_html(self, source):
        """Load html file and return data.

        :param source: source file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_html(source)

    def __read_tsv(self, source, sep='\t'):
        """Load tsv file and return data.

        :param source: source file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(source, sep=sep)
