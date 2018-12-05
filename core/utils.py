"""Image Comparison Module using Structural Similary and Open CV."""
import cv2
from skimage.measure import compare_ssim as ssim
#import matplotlib.pyplot as plt
import numpy as np
import traceback



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

            #Uncomment the following code if you want to use matplot lib to see the image difference.
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

            #Uncomment the following code if you want to use matplot lib to see the image difference.

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
    

    
