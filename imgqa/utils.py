"""Image Comparison Module using Structural Similary and Open CV."""
from PIL import Image
import pytesseract


class CrackCaptcha:
    """Extract the text from image presented."""

    def captcha_to_text(self, imagepath):
        """Method to return extracted text from passed image."""
        return pytesseract.image_to_string(Image.open(imagepath))
