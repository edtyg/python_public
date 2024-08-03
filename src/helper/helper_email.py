"""
Helper to send emails
Allows for attachments and dataframes in body
"""

import smtplib
from email import encoders
from email.mime.base import MIMEBase  # use this for files
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # use this for text

from pretty_html_table import build_table


class EmailHelper:
    """
    Helper class for sending Emails
    """

    @staticmethod
    def send_email(
        email_user: str,
        email_password: str,
        email_recipients: list,
        subject: str,
        message: str = None,
        list_of_df: list = None,
        attachments_directory=None,
        list_of_attachments=None,
    ):
        """sends email that allows Dataframes in message"""
        username = email_user
        password = email_password
        server = "smtp.office365.com:587"
        recipient = email_recipients

        message = MIMEMultipart()
        message["Subject"] = subject  # subject
        message["From"] = username
        message["To"] = ", ".join(recipient)

        ### Adding Messages to Body ###

        ### Printing Dataframes to message ###
        output = None
        if list_of_df:
            for df in list_of_df:
                table = build_table(df, "green_light", font_size="small")
                if output == None:
                    output = table
                else:
                    output += table

            # attach tables to message
            message.attach(MIMEText(output, "html"))

        if list_of_attachments is not None:
            for i in list_of_attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(attachments_directory + i, "rb").read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={i}")
                message.attach(part)  # attachments

        server = smtplib.SMTP(server)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(email_user, email_recipients, message.as_string())
        server.quit()
        print("Email Sent")
