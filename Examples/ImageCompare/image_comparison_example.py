from imgqa.core.utils import ImageCompare
import cv2

# Variable Stack / Data
img1 = cv2.imread("highway.jpg")
img2 = cv2.imread("highway_altered.jpg")
img3 = cv2.imread("sea.jpg")


class TestImageCompare(ImageCompare):
    """Sample Test Suite."""

    def test_compare_images(self):
        # Considering the width and ensuring dimesion to be same
        width = 2160
        # keep original height
        height = img2.shape[0]
        dim = (width, height)
        # resizing altered image2
        resized_img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
        height = 3840
        dim = (width, height)
        # resizing altered image3
        resized_img3 = cv2.resize(img3, dim, interpolation=cv2.INTER_AREA)

        self.grayscaling_images_and_comparing(img1, resized_img2)
        # self.image_compare_thru_opencv(img1, resized_img2)
