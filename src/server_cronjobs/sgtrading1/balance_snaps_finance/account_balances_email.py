"""
sending emails
"""

import datetime as dt
import os

import pandas as pd
from sqlalchemy import text

from helper.helper_config import ConfigHelper
from helper.helper_email import EmailHelper
from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from server_cronjobs.sgtrading1.balance_snaps_finance.misc.sqlalchemy_client import (
    SqlAlchemyConnector,
)

if __name__ == "__main__":
    # postgres database connector
    sql_client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    sql_client.postgres_connection()

    # query database and save results in excel file
    curr_time = dt.datetime.now()
    curr_time_before = curr_time + dt.timedelta(minutes=-30)
    curr_time_after = curr_time + dt.timedelta(minutes=30)

    query = f"""
    select * from account_balances where datetime >= '{str(curr_time_before)}' and datetime <= '{str(curr_time_after)}' order by datetime DESC
    """
    result = sql_client.connection.execute(text(query))
    df_result = pd.DataFrame(result)
    print(df_result)

    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    filename = "account_balances.xlsx"

    writer = pd.ExcelWriter(save_path + filename)
    df_result.to_excel(writer, sheet_name="account_balances")
    writer.close()
    print("file Saved")

    # send emails
    email_cred_config = "/home/edgar/python/config/others/emails/email_credentials.ini"
    email_recipients_config = (
        "/home/edgar/python/config/others/emails/email_recipients.ini"
    )

    email_config = ConfigHelper.get_section_data(email_cred_config, "otc_report")
    email_recipient = ConfigHelper.get_section_data(
        email_recipients_config, "balance_snaps"
    )
    print(list(email_recipient.values()))

    EmailHelper.send_email(
        email_user=email_config["username"],
        email_password=email_config["password"],
        email_recipients=list(email_recipient.values()),
        subject="Account Balances",
        list_of_df=None,
        attachments_directory=save_path,
        list_of_attachments=[filename],
    )
    print("email sent")
