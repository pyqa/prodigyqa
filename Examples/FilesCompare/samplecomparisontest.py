"""Example for Comparison module."""
from imgqa import Compare

# Variable Stack / Data
image1 = "highway.jpg"
image2 = "highway_altered.jpg"
source_xl = "source.xlsx"
target_xl = "target.xlsx"
source_csv = "source_csv.csv"
target_csv = "target_csv.csv"
source_json = "{'as': 1," \
              "'a': {'b': {'cs':10, 'qqq': {'qwe':1}}," \
              "'d': {'csd':30}}}"
target_json = "{'as': 1," \
              "'a': {'b': {'ds':10, 'qqq': {'qwe':11}}," \
              "'d': {'dsd':40}}}"


class TestCompareFiles(Compare):
    """Sample Test Suite."""

    def test_compare_images(self):
        """Compare images."""
        self.assertEqual(self.compare_images(image1, image1), 1.0)

    def test_compare_jsons(self):
        """Compare jsons."""
        self.assertNotEqual(self.compare_json(source_json, target_json), '{}')

    def test_compare_workbooks(self):
        """Compare spreadsheet.

        xl file will be generated with file difference.
        """
        self.compare_files(source_xl, target_xl)

    def test_compare_files(self):
        """Compare spreadsheet.

        xl file will be generated with file difference.
        """
        self.compare_files(source_csv, target_csv)
