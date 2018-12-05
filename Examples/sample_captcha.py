"""CAPTCHA reading Sample Test file."""

from imgqa.core.captcha import Captcha

# Variables

imgpath = "E:\Projects\imgqa\Images\example_01.png"


class TestClass(Captcha):
    """Sample Test Suite."""

    def test_read_captcha(self):
        """Get users from application."""
        self.captcharead(imgpath)
