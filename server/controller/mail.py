import smtplib, secrets
from flask import abort
from email.mime.text import MIMEText
from datetime import timedelta
from redis.exceptions import ConnectionError

from server import EMAIL_PASSWORD, EMAIL_ID
from server.model import Redis


def save_code_into_redis(email, auth_code):
    Redis.set(email, auth_code, timedelta(minutes=5))


def create_auth_code():
    code = secrets.choice(range(100000, 1000000))

    return code


def send_email(email):
    auth_code = create_auth_code()

    try:
        save_code_into_redis(email, auth_code)

    except ConnectionError:
        abort(500, "redis_error")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASSWORD)

    msg = MIMEText(str(auth_code))
    msg['Subject'] = "yally auth code"

    server.sendmail(EMAIL_ID, email, msg.as_string())
    server.quit()

