"""Image Comparison Module using Structural Similary and Open CV."""
from subprocess import check_output
from PIL import Image
import pytesseract


class crackcaptcha:

    def captcha_to_text(self, imagepath):

        return pytesseract.image_to_string(Image.open(imagepath))

        # Resampling the Image
        # check_output(['convert', imagepath, '-resample', '600', imagepath])
