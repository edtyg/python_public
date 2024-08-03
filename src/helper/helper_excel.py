"""
Helper to work with excel or csv files
"""

import os

import pandas as pd


class ExcelHelper:
    """
    Helper class to work with excel files using pandas
    """

    @staticmethod
    def read_excel_file(filepath: str):
        """Reads File as Pandas DataFrame"""
        df_excel = pd.read_excel(filepath)
        return df_excel

    def export_excel_file(filepath: str):
        pass


if __name__ == "__main__":
    pass
    folder_name = os.path.dirname(os.path.realpath(__file__))
    file_name = "/sample_file.xlsx"
    path = folder_name + file_name

    df = ExcelHelper.read_excel_file(path)
    print(df)

    # section_data = ConfigHelper.get_section_data(path, "otc_report")
    # print("section data here")
    # print(section_data)

    # ConfigHelper.add_section(path, "bnb-params")
    # ConfigHelper.delete_section(path, "bnb-params")

    # ConfigHelper.add_data(path, "bnb-params", "option2", "value1")
    # ConfigHelper.delete_data(path, "bnb-params", "option1")

    # ConfigHelper.modify_data(path, "bnb-params", "option2", "test")
