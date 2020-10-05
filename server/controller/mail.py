import smtplib, secrets
from flask import abort
from email.mime.text import MIMEText

from server import EMAIL_PASSWORD, EMAIL_ID
from server.model import Redis


def save_code_into_redis():
    pass


def create_auth_code():
    code = secrets.choice(range(100000, 1000000))

    return code


def send_email(email):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # 위 코드에서 에러남
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASSWORD)

    msg = MIMEText(f"{create_auth_code()}")
    msg['Subject'] = "yally 인증 코드"

    server.sendmail(EMAIL_ID, email, msg.as_string())
    server.quit()
