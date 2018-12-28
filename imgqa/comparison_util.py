# -*- coding: utf-8 -*-
"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
import pandas as pd
import cv2
from skimage.measure import compare_ssim as ssim
import numpy as np
import traceback
from json import JSONDecodeError
import os
import json
import matplotlib.pyplot as plt
import logging
import sys


class ImageCompare:
    """Image Comparison method class container."""

    images_equal = False
    images_same_size_channel = False
    mse_ssim_equality = True

    def image_compare_thru_opencv(self, first_image_path, second_image_path):
        r"""Compare two images using OpenCV library, on the basis of their shapes
        and b, g, r channels and return True/False depending on whether the
         two images are same or not.
        :param first_image_path: Path for the first image file to compare.
        :param second_image_path: Path for the second image file to compare.
        :return: True/False depending upon whether both images are same or not.
        :rtype: boolean
        """
        try:
            first_image_extenion = first_image_path.split(".")[1]
            second_image_extension = second_image_path.split(".")[1]

            if first_image_extenion not in ('jpg', 'jpeg', 'png') and \
                    second_image_extension not in ('jpg', 'jpeg', 'png'):
                logging.warning("Please provide correct file extensions "
                                "for image comparison.")
            # Reading the image files
            else:
                img1 = cv2.imread(first_image_path)
                img2 = cv2.imread(second_image_path)

                # keep original height
                width = 2160
                height = img2.shape[0]
                dim = (width, height)

                # resizing image2
                resized_img2 = cv2.resize(img2,
                                          dim,
                                          interpolation=cv2.INTER_AREA)

                img1_shape = img1.shape
                img2_shape = img2.shape

                if img1_shape == img2_shape:
                    images_same_size_channel = True
                    difference = cv2.subtract(img1, resized_img2)

                    b, g, r = cv2.split(difference)
                    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 \
                            and cv2.countNonZero(r) == 0:
                        images_equal = True
                    else:
                        images_equal = False

                else:
                    images_same_size_channel = False

                # Following is to close the open windows for any analysis
                # presentation. Mostly unsued while running through CLI.
                # self._visual_difference(difference)

                if images_same_size_channel is True and images_equal is True:
                    return True

                else:
                    return False
        except Exception:
            logging.warning("There is some issue in image comparison.")

    def _visual_difference(self, difference):
        cv2.imshow("difference", difference)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __mse(self, img1, img2):
        try:
            # the 'MSE(Mean Squared Error)' between the two images is the
            # sum of the squared difference between the two images;
            # NOTE: the two images must have the same dimension
            err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
            err /= float(img1.shape[0] * img1.shape[1])

            # return the MSE, the lower the error, the more "similar"
            # the two images are
            return err
        except Exception:
            traceback.print_exc()

    def __mse_ssim_comparison(self, img1, img2):

        mse_sssim_vals = []

        """SSIM and Mean Squared Error Comparison."""
        try:
            # compute the mean squared error and structural similarity
            # index for the images
            mse_val = self.__mse(img1, img2)
            ssim_val = ssim(img1, img2)

            if mse_val == 0.00 and ssim_val == 1.00:
                mse_ssim_equality = True
                mse_sssim_vals.append(mse_ssim_equality)
            elif mse_val > 0 and ssim_val < 1:
                mse_ssim_equality = False
                mse_sssim_vals.append(mse_ssim_equality)
                mse_sssim_vals.append(mse_val)
                mse_sssim_vals.append(ssim_val)

            # Uncomment the following code if you want to use matplot
            # lib to see the image difference.
            # self._image_difference_thru_matplotlib\
            #     (mse_val,ssim_val, img1, img2, "first vd second")

            return mse_sssim_vals
        except Exception:
            traceback.print_exc()

    def _image_difference_thru_matplotlib(self, mse_val,
                                          ssim_val,
                                          img1,
                                          img2,
                                          title):
        # setup the figure
        fig = plt.figure(title)
        plt.suptitle("MSE: %.2f, SSIM: %.2f" % (mse_val, ssim_val))

        # show first image
        fig.add_subplot(1, 2, 1)
        plt.imshow(img1, cmap=plt.cm.gray)
        plt.axis("off")

        # show the second image
        fig.add_subplot(1, 2, 2)
        plt.imshow(img2, cmap=plt.cm.gray)
        plt.axis("off")

        # show the images
        plt.show()

    def grayscaling_and_comparing_images_thru_mse_ssim(self,
                                                       first_image_path,
                                                       second_image_path):
        r"""Compare two images on the basis mse and ssim index and returns
        a list containing True/False depending on whether 2 images are same
        or not, mse value and ssim value.
        :param first_image_path: Path for the first image file to compare.
        :param second_image_path: Path for the second image file to compare.
        :return: list containing True/False depending on whether 2 images
        are same or not, mse value and ssim value.
        :rtype: list
        """
        try:
            first_image_extenion = first_image_path.split(".")[1]
            second_image_extension = second_image_path.split(".")[1]

            if first_image_extenion not in ('jpg', 'jpeg', 'png') and \
                    second_image_extension not in ('jpg', 'jpeg', 'png'):
                logging.warning("Please provide correct file extensions "
                                "for image comparison.")
            # Reading the image files
            else:
                img1 = cv2.imread(first_image_path)
                img2 = cv2.imread(second_image_path)

                # keep original height
                width = 2160
                height = img2.shape[0]
                dim = (width, height)

                # resizing image2
                resized_img2 = cv2.resize(img2,
                                          dim,
                                          interpolation=cv2.INTER_AREA)

                # convert the images to grayscale
                first_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                second_img = cv2.cvtColor(resized_img2, cv2.COLOR_BGR2GRAY)

                # Uncomment the following code if you want to use matplot
                #  lib to see the image difference.
                # self._comparing_images_visually_thru_matplotlib(first_img,
                #                                                 second_img)

                # compare the images
                self.__mse_ssim_comparison(first_img, second_img)
        except Exception:
            logging.warning("There is some issue in image comparison.")

    def _comparing_images_visually_thru_matplotlib(self, first, second):
        fig = plt.figure("Images")
        images = ("First", first), ("Second", second)
        for (i, (name, image)) in enumerate(images):
            # show the image
            ax = fig.add_subplot(1, 3, i + 1)
            ax.set_title(name)
            plt.imshow(image, cmap=plt.cm.gray)
            plt.axis("off")

        # show the figure
        plt.show()


class JsonCompare:

    def compare_json(self, first_json_path, second_json_path, path=""):
        r"""Compare two jsons and generates a text file containing the
            difference.
        :param first_json_path: Path for the first json file to compare.
        :param second_json_path: Path for the second json file to compare.
        :return: True/False depending upon whether both jsons are same or not.
        :rtype: boolean
        """
        are_json_different = True
        try:
            first_json_extenion = first_json_path.split(".")[1]
            second_json_extension = second_json_path.split(".")[1]
            if first_json_extenion not in ('json') and \
                    second_json_extension not in ('json'):
                logging.warning("Please provide correct file extensions "
                                "for json comparison.")
            # Reading the json files
            else:
                # Reading the jsons and converting them into dictionaries.
                with open(first_json_path) as first_json:
                    dict1 = json.load(first_json)
                with open(second_json_path) as second_json:
                    dict2 = json.load(second_json)

                if dict1 == dict2:
                    are_json_different = False
                else:
                    if path is "":
                        try:
                            os.remove("json_diff.txt")
                        except OSError:
                            pass
                    for k in dict1.keys():
                        # Checking whether some key present in one dictionary
                        # is not present in other dictionary.
                        if k not in dict2.keys():
                            keydiff = (str(k) + " as key not in d2")
                            with open('json_diff.txt', 'a') as the_file:
                                the_file.write(str(keydiff))
                        else:
                            if type(dict1[k]) is dict:
                                if path == "":
                                    path = k
                                else:
                                    path = path + "->" + k
                                # Making recursive call by passing
                                # the keys which are present
                                # as dictionary object.
                                self.compare_json(dict1[k], dict2[k], path)
                            else:
                                if dict1[k] != dict2[k]:
                                    keystr = (str(path), ":")
                                    first_file_val = " First file ", k, " : ",\
                                                     dict1[k]
                                    second_file_val = " Second file ", k,\
                                                      " : ", dict2[k]

                                    # Writing the difference to the file.
                                    with open('json_diff.txt', 'a') \
                                            as the_file:
                                        the_file.write(str(keystr) + '\n')
                                        the_file.write(str(first_file_val) +
                                                       '\n')
                                        the_file.write(str(second_file_val) +
                                                       '\n')
                                        the_file.write('\n')
            return are_json_different
        except JSONDecodeError:
            logging.warning("Invalid json. Please provide file with proper"
                            " json structure.")
        except Exception:
            logging.warning("There is some issue in json comparison.")


class SpreadsheetCompare:

    def compare_excel(self, first_excel_path, second_excel_path):
        r"""Compare two excels and generates an excel file containing the
        difference. If resultant excel file contain empty cell that means
        the value is same in both excels else not.
        :param first_excel_path: Path for the first excel file to compare.
        :param second_excel_path: Path for the second excel file to compare.
        :return: True/False depending upon whether both excels are same or not.
        :rtype: boolean
        """
        are_excels_different = True
        try:
            first_excel_extenion = first_excel_path.split(".")[1]
            second_excel_extension = second_excel_path.split(".")
            [1]
            if first_excel_extenion not in ('xls', 'xlsx') and\
                    second_excel_extension not in ('xls', 'xlsx'):
                logging.warning("Please provide correct file "
                                "extensions for excel comparison.")
            # Reading the excel files
            else:
                excel1 = pd.read_excel(first_excel_path,
                                       encoding=sys.getfilesystemencoding())
                excel2 = pd.read_excel(second_excel_path,
                                       encoding=sys.getfilesystemencoding())

                # Checking if the excels are empty
                if excel1.empty is True and excel2.empty is True:
                    logging.warning("The excel files are empty")

                # Checking whether the no.of rows is same in both excels.
                elif len(excel1) != len(excel2):
                    logging.warning("The no. of rows in both "
                                    "excel are not same")

                # Checking whether the no.of columns is same in both excels.
                elif len(excel1.columns) != len(excel2.columns):
                    logging.warning("The no. of columns in both "
                                    "excel are not same")
                else:
                    # Setting column order same in both excels.
                    excel1.columns = excel2.columns

                    # Sorting excel data on the basis of a column.
                    excel1 = excel1.sort_values(
                        'id', ascending=False).reset_index(inplace=False)
                    excel2 = excel2.sort_values(
                        'id', ascending=False).reset_index(inplace=False)

                    # Getting the difference in data between both excels.
                    difference = excel1[excel1 != excel2]
                    if (difference.isnull().values.all()) is True:
                        are_excels_different = False

                    # Writing the delta between both excels in a separate
                    # excel file.
                    writer = pd.ExcelWriter(
                        'excel_diff.xlsx', engine='xlsxwriter')
                    difference.to_excel(writer,
                                        sheet_name='sheet1',
                                        index=False,
                                        encoding=sys.getfilesystemencoding())
            return are_excels_different
        except Exception:
            logging.warning("There is some issue in excel comparison.")
