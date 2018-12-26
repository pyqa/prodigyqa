| Method Name        | Description           | Args  | Usage |
| ------------- |:-------------:| -----:| -----: |
| image_compare_thru_opencv     | This method checks for difference in blue, green and red channels of the 2 images and return boolean value accordingly. | a) First image to compare  b)Second image to compare | self.image_compare_thru_opencv(img1, resized_img2)     | 
| grayscaling_images_and_comparing      | This method grayscales both the images and call mse and ssim comparison methods to compare both images.    |   a) First image to compare  b)Second image to compare |  self.grayscaling_images_and_comparing(img1, resized_img2)      |
