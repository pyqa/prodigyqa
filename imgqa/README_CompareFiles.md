| Method Name        | Description           | Args  | Usage |
| ------------- |:-------------:| -----:| -----: |
| compare_images     | This method calculates mse, ssim values for 2 images, also checks difference in b, g, r channels of the images and finally returns a dictionary object containing mse, ssim values and 2 boolean values on the basis of cv and mse/ssim comparison . | a) First image to compare  b)Second image to compare | self.compare_images(img1_path,
                            img2_path)     | 
| grayscaling_images_and_comparing      | This method grayscales both the images and call mse and ssim comparison methods to compare both images.    |   a) First image to compare  b)Second image to compare |  self.grayscaling_images_and_comparing(img1, resized_img2)      |
