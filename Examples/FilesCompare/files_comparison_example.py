"""Example for Comparison module."""
from imgqa import Compare

# Variable Stack / Data
img1_path = "highway.jpg"
img2_path = "highway_altered.jpg"
img3_path = "sea.jpg"
excel1_path = "first.xlsx"
excel2_path = "second.xlsx"
csv1_path = "first.csv"
csv2_path = "second.csv"
json1 = {'a': 2, 'b': 1, 'c': 0}
json2 = {'b': 2, 'c': 0}


class TestCompareFiles(Compare):
    """Sample Test Suite."""

    # def test_compare_images(self):
    #     """Compare images."""
    #     self.compare_images(img1_path, img2_path)

    def test_compare_jsons(self):
        """Comparing jsons."""
        dict_diff = self.compare_json(json1, json2)
        print(dict_diff)
        print(type(dict_diff))
        print(len(dict_diff))

    # def test_compare_spreadsheet(self):
    #     """Compare spreadsheet."""
    #     self.compare_files(excel1_path, excel2_path)
