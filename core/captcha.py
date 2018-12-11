from subprocess import check_output
from PIL import Image
import sys
import pytesseract


class Captcha:

    def captchaRead(self, imagepath=None):

        if imagepath is None:
            print('Please give Image path in the function defined in sample_captcha.py file')
            sys.exit(1)

        #Resampling the Image
        check_output(['convert', imagepath, '-resample', '600', imagepath])
        
        #Returning the captcha text in the form of string.
        return pytesseract.image_to_string(Image.open(imagepath))
