"""Useful Utilities which are used across modules will be put here."""

from PIL import Image

import pytesseract


class Utilities(object):
    """Utilities to contain few random methods which are easy and reusable."""

    def captcha_to_text(self, image):
        """Method to return extracted text from passed image."""
        return pytesseract.image_to_string(Image.open(image))
    
    def is_string(self, item):
        if isinstance(item, str):
            return True
        else:
            return False
    
    def is_ok(self, item):
        if is_string(item):
            return item.upper() not in ('FALSE', 'NO', '', 'NONE', '0', 'OFF')
        return bool(item)


    def is_not_ok(self, item):
        return not is_truthy(item)

    def is_none(self, item):
        return item is None or is_string(item) and item.upper() == 'NONE'

   

    

