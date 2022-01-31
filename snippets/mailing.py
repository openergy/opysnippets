"""
opysnippets/mailing:1.0.0
"""
import os
import datetime as dt

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


class EmailingClient:
    def __init__(self, default_sender, server, port, username, password, tls=True):
        self._default_sender = default_sender
        self._server = server
        self._port = port
        self._username = username
        self._password = password
        self._tls = tls

    def send(self, recipients_list, subject, text="", html="", attachments_d=None, sender=None):
        send_mail(
            sender if sender is not None else self._default_sender,
            recipients_list,
            self._server,
            self._port,
            password=self._password,
            username=self._username,
            text=text,
            html=html,
            subject=subject,
            attachments_dict=attachments_d if attachments_d is not None else {},
            isTls=self._tls
        )


class MockEmailingClient:
    def __init__(self, default_sender, mails_dir):
        self._default_sender = default_sender
        os.makedirs(mails_dir, exist_ok=True)
        self._mails_dir = mails_dir

    def send(self, recipients_list, subject, text="", html="", attachments_d=None, sender=None):
        name = f"{dt.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')} - {', '.join(recipients_list)}"
        with open(os.path.join(self._mails_dir, name), "w") as f:
            msg = _get_msg(
                sender if sender is not None else self._default_sender,
                recipients_list,
                text=text,
                html=html,
                subject=subject,
                attachments_dict=attachments_d if attachments_d is not None else {},
            )
            f.write(msg.as_string())
        if html:
            with open(os.path.join(self._mails_dir, f"{name}.html"), "w") as f:
                f.write(html)
        if text:
            with open(os.path.join(self._mails_dir, f"{name}.txt"), "w") as f:
                f.write(text)


def send_mail(
        sender,
        recipients_list,
        server,
        port,
        password=None,
        username=None,
        text="",
        html="",
        subject="",
        attachments_dict=None,
        isTls=True
):
    """

    Parameters
    ----------
    sender: str
        email address of the sender

    recipients_list: list of str
        list of recipients mail addresses

    subject: str
        subject of the mail

    text: str
        plain text in the body of the mail

    html: str
        html string in the body of the mail (appears under the text)

    attachments_dict: dict
        a dict containing mail attachments
        dict keys are file_names
        dict values are file content in bytes

    server: str
        mail server used to send mail

    port: int
        port for mail server

    password: str, default None
        password to connect the sender mail account

    username: str, default None
        the username to connect the sender mail account
        if None, equal to the sender address

    isTls: bool, default True


    Returns
    -------

    """

    if username is None:
        username = sender
    if attachments_dict is None:
        attachments_dict = {}

    msg = _get_msg(sender, recipients_list, text=text, html=html, subject=subject, attachments_dict=attachments_dict)

    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, recipients_list, msg.as_string())
    smtp.quit()


def _get_msg(
    sender,
    recipients_list,
    text="",
    html="",
    subject="",
    attachments_dict=None
):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = ",".join(recipients_list)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    # attach text
    part_text = MIMEText(text, 'plain')
    msg.attach(part_text)

    # attach html
    part_html = MIMEText(html, 'html')
    msg.attach(part_html)

    for file_name, content_bytes in attachments_dict.items():
        part = MIMEBase("application", "octet-stream")
        part.set_payload(content_bytes)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={file_name}")
        msg.attach(part)

    return msg
