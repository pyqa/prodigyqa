"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
import pathlib
import pandas as pd
import cv2
from skimage.measure import compare_ssim as ssim
# import matplotlib.pyplot as plt
import numpy as np
import traceback
from json import JSONDecodeError
import os
import json


class ImageCompare:
    """Image Comparison method class container."""

    images_equal = False
    images_same_size_channel = False
    mse_ssim_equality = True

    def image_compare_thru_opencv(self, img1, img2):
        """Images blue, green and red channel compare through OpenCV Modules."""
        try:
            img1_shape = img1.shape
            img2_shape = img2.shape

            if img1_shape == img2_shape:
                images_same_size_channel = True
                difference = cv2.subtract(img1, img2)

                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    images_equal = True
                else:
                    images_equal = False

            else:
                images_same_size_channel = False

            # This is to close the open windows for any analysis presentation
            # Mostly unsued while running through CLI

            # Uncomment the following code if you have GUI available and want to see the image difference.
            # cv2.imshow("difference", difference)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            if images_same_size_channel is True and images_equal is True:
                return True

            else:
                return False
        except Exception:
            traceback.print_exc()

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

            # Uncomment the following code if you want to use matplot lib to see the image difference.
            # # setup the figure
            # fig = plt.figure(title)
            # plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
            #
            # # show first image
            # ax = fig.add_subplot(1, 2, 1)
            # plt.imshow(imagea, cmap=plt.cm.gray)
            # plt.axis("off")
            #
            # # show the second image
            # ax = fig.add_subplot(1, 2, 2)
            # plt.imshow(imageb, cmap=plt.cm.gray)
            # plt.axis("off")
            #
            # # show the images
            # plt.show()
            return mse_sssim_vals
        except Exception:
            traceback.print_exc()

    def grayscaling_images_and_comparing(self, img1, img2):
        """Grayscale the recieved images and compare using SSIM and MSE."""
        try:
            # convert the images to grayscale
            first_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            second_img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # Uncomment the following code if you want to use matplot lib to see the image difference.

            # # initialize the figure
            # fig = plt.figure("Images")
            # images = ("First", first), ("Second", second)
            #
            # # loop over the images
            # for (i, (name, image)) in enumerate(images):
            #     # show the image
            #     ax = fig.add_subplot(1, 3, i + 1)
            #     ax.set_title(name)
            #     plt.imshow(image, cmap=plt.cm.gray)
            #     plt.axis("off")
            #
            # # show the figure
            # plt.show()

        # compare the images
            self.__mse_ssim_comparison(first_img, second_img)
        except Exception:
            traceback.print_exc()


class JsonCompare:

    def compare_json(self, file1, file2, path=""):
        try:
            # Reading the jsons and converting them into dictionaries.
            with open(file1) as first_json:
                dict1 = json.load(first_json)
            with open(file2) as second_json:
                dict2 = json.load(second_json)

            if path is "":
                try:
                    os.remove("../Examples/json_diff.txt")
                except OSError:
                    pass
            for k in dict1.keys():
                # Checking whether some key present in one dictionary is not present in other dictionary.
                if not k in dict2.keys():
                    keydiff = (str(k) + " as key not in d2")
                    with open('../Examples/json_diff.txt', 'a') as the_file:
                        the_file.write(str(keydiff))
                else:
                    if type(dict1[k]) is dict:
                        if path == "":
                            path = k
                        else:
                            path = path + "->" + k
                        # Making recursive call by passing the keys which are present as dictionary object.
                        self.compare_json(dict1[k], dict2[k], path)
                    else:
                        if dict1[k] != dict2[k]:
                            keystr = (str(path), ":")
                            first_file_val = " First file ", k, " : ", dict1[k]
                            second_file_val = " Second file ", k, " : ", dict2[k]

                            # Writing the difference to the file.
                            with open('../Examples/json_diff.txt', 'a') as the_file:
                                the_file.write(str(keystr) + '\n')
                                the_file.write(str(first_file_val) + '\n')
                                the_file.write(str(second_file_val) + '\n')
                                the_file.write('\n')
        except JSONDecodeError:
            print("Invalid json. Please provide file with proper json structure.")
            quit()
        except Exception:
            traceback.print_exc()

class ExcelCompare:

    def compare_excel(self, file1, file2):
        try:
            # Reading the excel files
            excel1 = pd.read_excel(file1)
            excel2 = pd.read_excel(file2)

            # Checking if the excels are empty
            if excel1.empty == True and excel2.empty == True:
                print("The excel files are empty")
                quit()

            # Checking whether the no.of rows is same in both excels.
            elif len(excel1) != len(excel2):
                print("The no. of rows in both excel is not same")
                quit()

            # Checking whether the no.of columns is same in both excels.
            elif len(excel1.columns) == len(excel2.columns):
                print("The no. of columns in both excel is not same")
                quit()
            else:
                # Setting coulmn order same in both excels.
                excel1.columns = excel2.columns

                # Sorting excel data on the basis of a column.
                excel1 = excel1.sort_values(
                    'id', ascending=False).reset_index(inplace=False)
                excel2 = excel2.sort_values(
                    'id', ascending=False).reset_index(inplace=False)

                #Getting the difference in data between both excels.
                difference = excel1[excel1 != excel2]

                # Writing the delta between both excels in a seperate excel file.
                writer = pd.ExcelWriter(
                    '../Examples/excel_diff.xlsx', engine='xlsxwriter')
                difference.to_excel(writer, sheet_name='sheet1', index=False)
        except Exception:
            traceback.print_exc()




class CompareFiles(ImageCompare, JsonCompare, ExcelCompare):

    def files_to_compare(self, file1, file2):
        supported_formats = ('.xls', '.xlsx', '.png', '.jpeg', '.jpg','.json')

        # Checking whether the 2 input files belong to supported formats.
        if ''.join(pathlib.Path(file1).suffixes) not in supported_formats and \
                ''.join(pathlib.Path(file2).suffixes) not in supported_formats:
            print("Not a supported file format.")
        elif ''.join(pathlib.Path(file1).suffixes) in ('.xls', '.xlsx') and\
                ''.join(pathlib.Path(file2).suffixes) in ('.xls', '.xlsx'):
            ExcelCompare.compare_excel(file1, file2)
        elif ''.join(pathlib.Path(file1).suffixes) in ('.png', '.jpeg', '.jpg') and\
                ''.join(pathlib.Path(file2).suffixes) in ('.png', '.jpeg', '.jpg'):
            img1 = cv2.imread(file1)
            img2 = cv2.imread(file2)

            # keep original height
            width = 2160
            height = img2.shape[0]
            dim = (width, height)

            # resizing image2
            resized_img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
            ImageCompare.image_compare_thru_opencv(self, img1, resized_img2)
        elif ''.join(pathlib.Path(file1).suffixes) in ('.json') and \
                        ''.join(pathlib.Path(file2).suffixes) in ('.json'):
            JsonCompare.compare_json(file1, file2)
