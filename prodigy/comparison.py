# -*- coding: utf-8 -*-
"""Comparison Module for Images, Files like CSV, Excel, PDF etc."""
import unittest
import cv2
from skimage.measure import compare_ssim as ssim
import logging
import pandas as pd
from jsondiff import diff
import os


class Compare(unittest.TestCase):
    """File Comparison module which includes image, csv and workbook."""

    def __init__(self, *args, **kwargs):
        """Variable Stack Declaration."""
        super(Compare, self).__init__(*args, **kwargs)
        self.source = None
        self.target = None
        self.source_extn = None
        self.target_extn = None
        self.source_name = None
        self.target_name = None
        self.image_extn = ('jpg', 'jpeg', "png")
        self.excel_extn = ('xls', 'xlsx')
        self.file_extn = ('xls', 'xlsx', 'csv', 'tsv', 'hdf', 'html')

    def compare_images(self, source, target):
        """Compare images and returns structural similarity over the image.

        Measure of SSIM is returned between 0-1.0 where 1.0 is
        the most identical
        and 0 being completely different
        :param source: source image path.
        :param target: target image path.
        :return: SSIM difference of images which ranges between 0 and 1
        :rtype: float
        """
        self.source = cv2.imread(source)
        self.target = cv2.imread(target)
        self.source_extn = source.split(".")[1]
        self.target_extn = target.split(".")[1]
        if self.source_extn and self.target_extn not in self.image_extn:
            logging.error("Invalid image extension")
        self.target = cv2.resize(
            self.target, (int(self.source.shape[1]),
                          int(self.source.shape[0])))
        return ssim(self.source, self.target, multichannel=True)

    def compare_json(self, source, target):
        """Compare json files.

        :param source: source json.
        :param target: target json.
        :return: difference of target compared to source
        :rtype: Dictionary
        """
        return diff(source, target)

    def compare_files(self, source, target):
        """Compare two files and return difference(if any).

        File Types Supported: xls or xlsx or html or hdf or csv or tsv
        :param source: Source file Path.
        :param target: Target file path.
        :return: file difference
        :rtype: data frame of file difference.
        """
        self.source = source
        self.target = target
        self.source_extn = source.split('.')[1]
        self.target_extn = target.split('.')[1]
        self.source_name = source.split('.')[0]
        self.target_name = target.split('.')[0]
        if self.source_extn and self.target_extn in self.file_extn:
            if self.source_extn and self.target_extn in self.excel_extn:
                return self.__compare_workbooks()
            else:
                self.source_data = self.__load_into_dataframe(source)
                self.target_data = self.__load_into_dataframe(target)
                return self.__compare_non_workbook_files()
        else:
            logging.error('File Extension not supported')

    def __compare_workbooks(self):
        """Compare two xls or xlsx files and return difference and boolean.

        :return: True/False.
        :rtype: bool.
        """
        source_df = pd.ExcelFile(self.source)
        target_df = pd.ExcelFile(self.target)

        if source_df.sheet_names == target_df.sheet_names:
            for sheet in source_df.sheet_names:
                self.__compare_sheets(sheet)

    def __compare_sheets(self, sheet, unique_col="account number"):
        """Compare sreadsheets and return difference to xl file.

        :param sheet: sheet name
        :param unique_col: column name
        :return:
        """
        source_df = pd.read_excel(self.source, sheet).fillna('NA')
        target_df = pd.read_excel(self.target, sheet).fillna('NA')
        file_path = os.path.dirname(self.source)

        column_list = source_df.columns.tolist()

        source_df['version'] = "source"
        target_df['version'] = "target"

        source_df.sort_values(by=unique_col)
        source_df = source_df.reindex()
        target_df.sort_values(by=unique_col)
        target_df = target_df.reindex()

        # full_set = pd.concat([source_df, target_df], ignore_index=True)
        diff_panel = pd.concat([source_df, target_df],
                               axis='columns', keys=['df1', 'df2'],
                               join='outer', sort=False)
        diff_output = diff_panel.apply(self.__report_diff, axis=0)
        diff_output['has_change'] = diff_output.apply(self.__has_change)

        full_set = pd.concat([source_df, target_df], ignore_index=True)
        changes = full_set.drop_duplicates(subset=column_list, keep='last')
        dupe_records = changes.set_index(unique_col).index.unique()

        changes['duplicate'] = changes[unique_col].isin(dupe_records)
        removed_parts = changes[(~changes["duplicate"]) & (
            changes["version"] == "source")]
        new_part_set = full_set.drop_duplicates(
            subset=column_list, keep='last')
        new_part_set['duplicate'] = new_part_set[unique_col].isin(dupe_records)
        added_parts = new_part_set[(~new_part_set["duplicate"]) & (
            new_part_set["version"] == "target")]

        # Save the changes to excel but only include the columns we care about
        diff_file = file_path + "file_diff.xlsx"
        if os.path.exists(diff_file):
            os.remove(diff_file)
        writer = pd.ExcelWriter(file_path + "file_diff.xlsx")
        diff_output.to_excel(writer, "changed")
        removed_parts.to_excel(
            writer, "removed", index=False, columns=column_list)
        added_parts.to_excel(writer, "added", index=False, columns=column_list)
        writer.save()

    def __report_diff(self, x):
        """Report data difference.

        :param x:
        :return: difference
        """
        return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

    def __has_change(self, row):
        """Return Yes if cell has different data else No.

        :param row: row data
        :return: Yes/No
        """
        if "--->" in row:
            return "Yes"
        else:
            return "No"

    def __compare_non_workbook_files(self):
        """Return xl of spreadsheet difference.

        :return: True/False.
        :rtype: bool.
        """
        df = pd.concat([self.source_data, self.target_data])
        df = df.reset_index(drop=True)
        df_groupby = df.groupby(list(df.columns))
        index = [x[0] for x in df_groupby.groups.values() if len(x) == 1]
        diff = df.reindex(index)

        # Save the changes to excel
        file_path = os.path.dirname(self.source)
        diff_file = file_path + "file_diff.xlsx"
        if os.path.exists(diff_file):
            os.remove(diff_file)
        writer = pd.ExcelWriter(file_path + "file_diff.xlsx")
        diff.to_excel(writer, "difference")
        writer.save()

    def __load_into_dataframe(self, data):
        """Load hdf or csv or tsv file and return data.

        :param data: file.
        :return: file data.
        :rtype: data frame.
        """
        if data.split(".")[1] == 'csv':
            return self.__read_csv(data)
        elif data.split(".")[1] == 'hdf':
            return self.__read_hdf(data)
        elif data.split(".")[1] == 'html':
            return self.__read_html(data)
        elif data.split(".")[1] == 'tsv':
            return self.__read_tsv(data)

    def __read_csv(self, data, sep=None):
        """Load csv file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(data)

    def __read_hdf(self, data):
        """Load hdf file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_hdf(data)

    def __read_html(self, data):
        """Load html file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_html(data)

    def __read_tsv(self, data, sep='\t'):
        """Load tsv file and return data.

        :param data: data file path
        :return: file data.
        :rtype: data frame.
        """
        return pd.read_csv(data, sep=sep)
