"""
script for sending emails
"""
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import setting_1
import pandas as pd
from pretty_html_table import build_table

from local_credentials.api_key_others import EMAIL_USER, EMAIL_PASSWORD


class SendEmails:
    """class for sending emails"""

    def __init__(self, email_address: str, email_address_password: str, settings: dict):
        self.my_email_address = email_address
        self.my_email_address_password = email_address_password

        # self.server = "smtp.live.com:587"
        self.server = "smtp.office365.com:587"

        self.email_subject = settings["subject"]  # subject of email
        self.email_body = settings["body"]  # body of email
        self.recipient = settings["recipient"]  # intended recipient
        self.recipient_cc = settings["recipient_cc"]  # intended recipient cc

        self.attachment_directory = settings["attachment_directory"]
        self.attachement_files = settings["attachment_files"]

        self.tables = settings["tables"]

    def send_email(self):
        """sending a standard email"""

        message = MIMEMultipart()
        message["Subject"] = self.email_subject
        message["From"] = self.my_email_address
        message["To"] = ", ".join(self.recipient)
        message["Cc"] = ", ".join(self.recipient_cc)

        server = smtplib.SMTP(self.server)
        server.ehlo()
        server.starttls()
        server.login(self.my_email_address, self.my_email_address_password)
        server.sendmail(self.my_email_address, self.recipient, message.as_string())
        server.quit()
        print("Email Sent")

    def send_email_attachments(self):
        """sending email with attachments"""

        message = MIMEMultipart()
        message["Subject"] = self.email_subject
        message["From"] = self.my_email_address
        message["To"] = ", ".join(self.recipient)
        message["Cc"] = ", ".join(self.recipient_cc)

        if self.attachement_files:
            for i in self.attachement_files:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(self.attachment_directory + i, "rb").read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={i}")
                message.attach(part)

        server = smtplib.SMTP(self.server)
        server.ehlo()
        server.starttls()
        server.login(self.my_email_address, self.my_email_address_password)
        server.sendmail(self.my_email_address, self.recipient, message.as_string())
        server.quit()
        print("Email Sent")

    def send_email_print_tables(self):
        """sending email - print tables in body"""

        message = MIMEMultipart()
        message["Subject"] = self.email_subject
        message["From"] = self.my_email_address
        message["To"] = ", ".join(self.recipient)
        message["Cc"] = ", ".join(self.recipient_cc)

        # adding dataframes to body of email
        output = self.email_body
        for i in self.tables:
            table = build_table(i, "green_light", font_size="small")
            output += table
        message.attach(MIMEText(output, "html"))  # message body in text

        server = smtplib.SMTP(self.server)
        server.ehlo()
        server.starttls()
        server.login(self.my_email_address, self.my_email_address_password)
        server.sendmail(self.my_email_address, self.recipient, message.as_string())
        server.quit()
        print("Email Sent")


if __name__ == "__main__":
    email_client = SendEmails(EMAIL_USER, EMAIL_PASSWORD, setting_1)

    # sending a basic email
    # email_client.send_email()

    # sending email with attachments
    # email_client.send_email_attachments()

    # send emails with tables
    email_client.send_email_print_tables()
