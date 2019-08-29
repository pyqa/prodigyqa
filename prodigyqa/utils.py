"""Useful Utilities which are used across modules will be put here."""

from PIL import Image

import pytesseract


class Utilities(object):
    """Utilities to contain few random methods which are easy and reusable."""

    def captcha_to_text(self, image):
        """Method to return extracted text from passed image."""
        return pytesseract.image_to_string(Image.open(image))

    def is_string(self, item) -> bool:
        """Evaluate if an item sent is string.
        :rtype: bool
        """
        if isinstance(item, str):
            return True
        else:
            return False

    def is_ok(self, item):
        """Evaluate if an item sent is OK."""
        if self.is_string(item):
            return item.upper() not in ('FALSE', 'NO', '', 'NONE', '0', 'OFF')
        return bool(item)

    def is_not_ok(self, item):
        """Evaluate if an item sent is NOT OK."""
        return not self.is_ok(item)

    def is_none(self, item):
        """Evaluate if an item sent is None."""
        return item is None or self.is_string(item) and item.upper() == 'NONE'

    def are_equal(self, source, target, ignore_case=True):
        """Evaluate if an two strings shared are equal."""
        if ignore_case:
            return source.lower() == target.lower()
        else:
            return source == target
