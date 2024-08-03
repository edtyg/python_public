"""
Pulls CME Datamine data thru SFTP (Winscp)
Files are stored in multiple folders
Use this script to locate the files and extract them into a target folder
"""

import os

import patoolib

if __name__ == "__main__":
    target_directory = "D:/CME_DATA_EXTRACTED"  # folder for extracted files

    file_directory = "D:/2024"  # RAW File path here
    months = os.listdir(file_directory)
    for month in months:
        month_filepath = file_directory + "/" + month
        days = os.listdir(month_filepath)
        for day in days:
            day_filepath = month_filepath + "/" + day + "/CRYPTOCURRENCY/0/"
            filename = os.listdir(day_filepath)
            final_filename = day_filepath + filename[0]
            print(final_filename)
            # Extracts file here
            patoolib.extract_archive(final_filename, outdir=target_directory)
