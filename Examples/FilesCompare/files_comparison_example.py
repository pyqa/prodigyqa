"""Example for Comparison module."""
from imgqa import CompareFiles

# Variable Stack / Data
img1_path = "highway.jpg"
img2_path = "highway_altered.jpg"
img3_path = "sea.jpg"
excel1_path = "first.xlsx"
excel2_path = "second.xlsx"
json1_path = "third.json"
json2_path = "fourth.json"


class TestCompareFiles(CompareFiles):
    """Sample Test Suite."""

    def test_compare_images(self):
        """Compare images."""
        self.compare_images(img1_path,
                            img2_path)

    def test_compare_jsons(self):
        """Comparing jsons."""
        self.compare_json(json1_path, json2_path)

    def test_compare_spreadsheet(self):
        """Compare spreadsheet."""
        self.compare_spreadsheet(excel1_path, excel2_path)
