import pathlib
from itertools import zip_longest
import xlrd
from openpyxl import load_workbook
from pandas import DataFrame
from ImageCompare import  ImageCompare as imcmp
import pandas as pd
import cv2

class CompareFiles:


   def files_to_compare(self, file1, file2):
       supported_formats = ('.xls', '.xlsx', '.png', '.jpeg', '.jpg')
       if ''.join(pathlib.Path(file1).suffixes) not in supported_formats and \
                       ''.join(pathlib.Path(file2).suffixes) not in supported_formats:
           print("Not a supported file format.")
       elif ''.join(pathlib.Path(file1).suffixes) in ('.xls', '.xlsx') and\
                       ''.join(pathlib.Path(file2).suffixes) in ('.xls', '.xlsx') :
           self._compare_excel(file1,file2)
       elif ''.join(pathlib.Path(file1).suffixes) in ('.png', '.jpeg', '.jpg') and\
                       ''.join(pathlib.Path(file2).suffixes) in ('.png', '.jpeg', '.jpg'):
           img1 = cv2.imread(file1)
           img2 = cv2.imread(file2)
           # keep original height
           width = 2160
           height = img2.shape[0]
           dim = (width, height)

           # resizing altered image
           resized_img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
           imcmp.image_compare_thru_opencv(self,img1,resized_img2)
     

   def _compare_excel(self, file1, file2):
      excel1 =  pd.read_excel(file1)
      excel2 = pd.read_excel(file2)
      excel1.columns = excel2.columns
      excel1 = excel1.sort_values('id', ascending=False).reset_index(inplace=False)
      excel2 = excel2.sort_values('id', ascending=False).reset_index(inplace=False)
      difference = excel1[excel1!=excel2]
      writer = pd.ExcelWriter('../Examples/excel_diff.xlsx', engine='xlsxwriter')
      difference.to_excel(writer, sheet_name='sheet1', index=False)


