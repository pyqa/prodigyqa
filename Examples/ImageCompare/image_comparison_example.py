from imgqa.core.comparison_util import CompareFiles
import cv2

# Variable Stack / Data
img1 = "highway.jpg"
img2 = "highway_altered.jpg"
img3 = "sea.jpg"
excel1 = "first.xlsx"
excel2 = "second.xlsx"
json1 = "first.json"
json2 = "second.json"


class TestCompareFiles(CompareFiles):
    """Sample Test Suite."""

    def test_compare_files(self):
        # Comparing images
        self.files_to_compare(img1, img2)
        # Comparing excels
        self.files_to_compare(excel1, excel2
        # Comparing jsons
        self.files_to_compare(json1, json2)
        
