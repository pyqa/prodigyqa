from imgqa import ImageCompare, JsonCompare, SpreadsheetCompare

# Variable Stack / Data
img1_path = "highway.jpg"
img2_path = "highway_altered.jpg"
img3_path = "sea.jpg"
excel1_path = "first.xlsx"
excel2_path = "second.xlsx"
json1_path = "first.json"
json2_path = "second.json"


class TestCompareImages(ImageCompare):
    """Sample Test Suite."""

    def test_compare_images(self):
        # Comparing images
        self.grayscaling_and_comparing_images_thru_mse_ssim(img1_path,
                                                            img2_path)


class TestCompareJsons(JsonCompare):
    """Sample Test Suite."""

    def test_compare_jsons(self):
        # Comparing images
        self.compare_json(json1_path, json2_path)


class TestCompareExcels(SpreadsheetCompare):
    """Sample Test Suite."""

    def test_compare_excels(self):
        # Comparing images
        self.compare_excel(excel1_path, excel2_path)



        
