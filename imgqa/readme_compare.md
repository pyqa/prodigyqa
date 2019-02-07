| Method Name        | Description           | Args  | Usage |
| ------------- |:-------------:| -----:| -----: |
| compare_images     | Compare images and returns structural similarity over the image. Measure of SSIM is returned between 0-1.0 where 1.0 is the most identical and 0 being completely different. | a) source image path.  b)target image path. | self.compare_images(source, target)     | 
| compare_json      | Compare json files and returns dictionary of difference of target compared to source.    |   a) source json.  b)target json |  self.compare_json(source, target)      |
| compare_files      | Compare two files and return xl of difference(if any). SupportedfFile Types are xls or xlsx csv    |   a) Source file Path.  b)target file Path. |  self.compare_files(source, target)      |
