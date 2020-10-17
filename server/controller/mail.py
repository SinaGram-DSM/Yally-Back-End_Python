import smtplib, secrets
from flask import abort
from email.mime.text import MIMEText
from datetime import timedelta
from redis.exceptions import ConnectionError

from server import EMAIL_PASSWORD, EMAIL_ID
from server.model import Redis


def save_code_into_redis(email, auth_code, codetype):
    Redis.set(email+codetype, auth_code, timedelta(minutes=5))


def create_auth_code():
    code = secrets.choice(range(100000, 1000000))

    return code


def send_code_to_email(email, codetype):
    code = create_auth_code()

    try:
        save_code_into_redis(email, code, codetype=codetype)

    except ConnectionError:
        abort(500, "redis_error")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASSWORD)

    msg = MIMEText(str(code))
    msg['Subject'] = f"yally {codetype} code"

    server.sendmail(EMAIL_ID, email, msg.as_string())
    server.quit()

    return



def send_auth_code_email(email):
    auth_code = create_auth_code()

    send_code_to_email(email, codetype="auth")

    return {
        "message": "Successfully send auth code"
    }


def send_reset_code_email(email):
    reset_code = create_auth_code()

    send_code_to_email(email, codetype="reset")

    return {
        "message": "Successfully send reset code"
    }


def send_email(email, codetype):
    if codetype == 'auth':
        return send_auth_code_email(email)
    elif codetype == 'reset':
        return send_reset_code_email(email)


