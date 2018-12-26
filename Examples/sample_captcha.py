"""CAPTCHA reading Sample Test file."""

from imgqa.utils import crackcaptcha

# Variable stack

imgpath = "OCR_Example_Image\\example_01.png"


class TestClass(crackcaptcha):
    """Sample Test Suite."""

    def test_read_captcha(self):
        """Get users from application."""
        print(self.captcharead(imgpath))
