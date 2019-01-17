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
from jsondiff import diff

class Compare(unittest.TestCase):
    """File Comparison module which includes image, csv and workbook."""

    def __init__(self, *args, **kwargs):
        """Variable Stack Declaration."""
        super(Compare, self).__init__(*args, **kwargs)
        self.source = None
        self.target = None
        self.source_extn = None
        self.target_extn = None
        self.source_name = None
        self.target_name = None
        self.image_extn = ('jpg', 'jpeg', "png")
        self.excel_extn = ('xls', 'xlsx')
        self.file_extn = ('xls', 'xlsx', 'csv', 'tsv', 'hdf', 'html')

    def compare_images(self, source, target):
        """Compare images on the basis mse and ssim index.

        :param source: source image path.
        :param target: target image path.
        :return: True/False.
        :rtype: bool.
        """
        self.source = cv2.imread(source)
        self.target = cv2.imread(target)
        self.source_extn = source.split(".")[1]
        self.target_extn = target.split(".")[1]
        if self.source_extn and self.target_extn not in self.image_extn:
            logging.warning("Invalid image extension")
            return False
        if self.__compare_images_structure() \
            and self.__compare_images_mse() \
                and self.__compare_images_ssim():
            logging.info("Images are Similar")
            return True
        else:
            logging.warning("Images are not Similar")
            self.__images_visual_difference()
            return False

    def __compare_images_structure(self):
        """Checkpoint to measure on size and shape of image.

        :param source: source image path.
        :param target: target image path.
        :return: True/False.
        :rtype: bool.
        """
        if self.source.shape == self.target.shape:
            logging.info("Images of same size")
            difference = cv2.subtract(self.source, self.target)
            b, g, r = cv2.split(difference)
            non_zero_b = cv2.countNonZero(b)
            non_zero_g = cv2.countNonZero(g)
            non_zero_r = cv2.countNonZero(r)
            if ((non_zero_b == non_zero_g) == non_zero_r) == 0:
                logging.info("Images are structurally equal")
                return True
            else:
                logging.warning("RGB Attributes are different\
                though images are same dimensions")
                return False
        else:
            logging.warning("The images have different size and channels")
            return False

    def __compare_images_mse(self):
        """Checkpoint to measure Mean Square Error (MSE) difference of images.

        :return: True/False.
        :rtype: bool.
        """
        mse_val = np.sum(
            (self.source.astype("float") - self.target.astype("float")) ** 2)
        mse_val /= float(self.source.shape[0] * self.source.shape[1])

        if mse_val == 0.00:
            logging.info("Source and target images have same MSE value")
            return True
        else:
            logging.warning(
                "MSE Value of both images: {0}" % mse_val)
            return False

    def __compare_images_ssim(self):
        """Measure Structural Similarity Index (SSIM) difference of images.

        :return: True/False.
        :rtype: bool.
        """
        ssim_val = ssim(self.source, self.target)
        if ssim_val == 1.00:
            logging.info("SSIM Value for compared images{0}" % ssim_val)
            return True
        else:
            logging.warning(
                "SSIM value for compared images: {0}" % ssim_val)
            return ssim_val

    def __images_visual_difference(self):
        """"Show the images visual difference.

        :return: NA
        :rtype: NA
        """
        difference = cv2.subtract(self.source, self.target)
        cv2.imshow("difference", difference)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def compare_json(self, source, target):
        """Compare json files.

        :param source: source json.
        :param target: target json.
        :return: difference of target compared to source
        :rtype: Dictionary
        """
        return diff(source, target)

    def compare_files(self, source, target):
        """Compare two files and return difference(if any).

        File Types Supported: xls or xlsx or html or hdf or csv or tsv
        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        self.source_extn = source.split('.')[1]
        self.target_extn = target.split('.')[1]
        self.source_name = source.split('.')[0]
        self.target_name = target.split('.')[0]
        self.source = source
        self.target = target
        if self.source_extn and self.target_extn in self.file_extn:
            if self.source_extn and self.target_extn in self.excel_extn:
                return self.__compare_workbooks()
            else:
                self.source = self.__load_into_dataframe(source)
                self.target = self.__load_into_dataframe(target)

                if self.source_extn and self.target_extn not in self.excel_extn:
                    return self.__compare_non_workbook_files()
                if self.self.source_extn or self.target_extn in self.excel_extn:
                    return self.__compare_spreadsheet_and_non_spreadsheet()
        else:
            logging.warning('File Extension not supported')
            return False

    def __compare_workbooks(self):
        """Compare two xls or xlsx files and return difference and boolean.

        :return: True/False.
        :rtype: bool.
        """
        source_dataframe = pd.ExcelFile(self.source)
        target_dataframe = pd.ExcelFile(self.target)
        flag = 0
        if source_dataframe.sheet_names == target_dataframe.sheet_names:
            source_sheets = source_dataframe.sheet_names
            for source_sheet in source_sheets:
                if source_dataframe.parse(source_sheet) == target_dataframe.parse(source_sheet):
                    logging.info("Spreadsheet '{0}' of " /
                                 "source '{1}' and target '{2}' have same data".format /
                                 (source_sheet, self.source_name, self.target_name))
                else:
                    difference = source_dataframe.parse(source_sheet)[source_dataframe.parse(
                        source_sheet) != target_dataframe.parse(source_sheet)]
                    logging.warning("Spreadsheet '{0}' of " /
                                    "source '{1}' and target '{2}' have different data\n {3}".format /
                                    (source_sheet, self.source_name, self.target_name, difference))
                    flag += 1
            if flag == 0:
                logging.info("Both source '{0}' and target '{1}' work" /
                             "books have same data".format(source_sheet,
                                                           self.source_name, self.target_name))
                return True
            else:
                logging.info("one or more spread sheets of source '{0}' and target '{1}'" /
                             "have different data".format(source_sheet, self.source_name, self.target_name))
                return False

    def __compare_non_workbook_files(self):
        """Compare two html or hdf or csv or tsv and return difference and boolean.

        :return: True/False.
        :rtype: bool.
        """
        difference = self.source_data[self.source_data != self.target_data]
        if difference == '':
            logging.info("Both source '{0}' and target '{1}'" /
                         "have same data".format(self.source_name, self.target_name))
            return True
        else:
            logging.warning("Source '{0}' and target '{1}'" /
                            "have different data\n {2}".format(self.source_name, self.target_name, difference))
            return False

    def __compare_spreadsheet_and_non_spreadsheet(self):
        """Compare two files of xls or xlsx and html or hdf or csv or tsv and return difference and boolean.

        :param source: Source file Path.
        :param target: Target file path.
        :return: True/False.
        :rtype: bool.
        """
        if self.source_extn in self.excel_extn and self.target_extn not in self.excel_extn:
            df = pd.ExcelFile(self.source)
            data = self.__load_into_dataframe(self.target)
        elif self.source_extn not in self.excel_extn and self.target_extn in self.excel_extn:
            df = pd.ExcelFile(self.target)
            data = self.__load_into_dataframe(self.source)
        for sheet in df.sheet_names:
            if df.parse(sheet) in data:
                logging.info("Both source '{0}' and target '{1}'" /
                             "have same data".format(self.source_name, self.target_name))
                break
        else:
            logging.warning("source '{0}' and target '{1}'" /
                            "have different data".format(self.source_name, self.target_name))
            return False
        return True

    def __load_into_dataframe(self, data):
        """Load hdf or csv or tsv file and return data.

        :param data: file.
        :return: file data.
        :rtype: data frame.
        """
        if data.split(".")[1] == 'csv':
            return self.__read_csv(data)
        elif data.split(".")[1] == 'hdf':
            return self.__read_hdf(data)
        elif data.split(".")[1] == 'html':
            return self.__read_html(data)
        elif data.split(".")[1] == 'tsv':
            return self.__read_tsv(data)

    def __read_csv(self, data, sep=None):
        """Load csv file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(data)

    def __read_hdf(self, data):
        """Load hdf file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_hdf(data)

    def __read_html(self, data):
        """Load html file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_html(data)

    def __read_tsv(self, data, sep='\t'):
        """Load tsv file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(data, sep=sep)
