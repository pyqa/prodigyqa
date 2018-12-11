"""CAPTCHA reading Sample Test file."""

from imgqa.core.captcha import Captcha

# Variables

imgpath = "OCR_Example_Image\\example_01.png"


class TestClass(Captcha):
    """Sample Test Suite."""

    def test_read_captcha(self):
        """Get users from application."""
        text_retrieved = self.captcharead(imgpath)
        print(text_retrieved)
