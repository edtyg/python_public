"""
settings for sending emails
"""
import os
import pandas as pd

current_directory = os.path.realpath(__file__)
save_path = os.path.dirname(current_directory) + "/attachments/"

df1 = pd.DataFrame({"a": 1, "b": 2}, index=[0, 1])
df2 = pd.DataFrame({"a": 1, "b": 2}, index=[0, 1])

setting_1 = {
    "subject": "testing email",
    "body": "Hi there",
    "recipient": ["edgartan93@hotmail.com"],
    "recipient_cc": ["edgartan1993@hotmail.com"],
    "attachment_directory": save_path,  # attachment directory
    "attachment_files": ["attachment_1.xlsx", "attachment_2.xlsx"],  # list of files
    "tables": [df1, df2],
}
