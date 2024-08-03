""" sending email with dataframes"""

import smtplib
from email import encoders
from email.mime.base import MIMEBase  # use this for files
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # use this for text

from pretty_html_table import build_table


def send_email(
    email_user: str,
    email_password: str,
    email_recipients: list,
    subject,
    df1,
    attachments_directory=None,
    list_of_attachments=None,
):
    """sends email with a dataframe format"""
    username = email_user
    password = email_password
    server = "smtp.office365.com:587"
    recipient = email_recipients

    message = MIMEMultipart()
    message["Subject"] = subject  # subject
    message["From"] = username
    message["To"] = ", ".join(recipient)

    table1 = build_table(df1, "green_light", font_size="small")
    output = table1
    message.attach(MIMEText(output, "html"))  # message body in text

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
