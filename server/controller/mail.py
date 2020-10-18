import smtplib, secrets
from flask import abort
from email.mime.text import MIMEText
from datetime import timedelta
from redis.exceptions import ConnectionError
from werkzeug.security import generate_password_hash

from server import EMAIL_PASSWORD, EMAIL_ID
from server.model import Redis, session
from server.model.user import User


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


def check_auth_code(email, code):
    auth_code = Redis.get(email+"auth").decode('utf-8')

    if auth_code == code:
        return {
            "message": "Successfully authenticated"
        }
    else:
        return abort(401, "The verification code is not correct")


def check_reset_code(email, code):
    reset_code = Redis.get(email + "reset").decode('utf-8')

    if reset_code == code:
        return True
    else:
        return False


def change_password(email, code, password):

    if check_reset_code(email, code):
        user = session.query(User).filter(User.email == email).first()

        if user:
            user.password = generate_password_hash(password)
            session.commit()

            return {
                "message": "Successfully password changed"
            }
        else:
            return abort(404, "The email is incorrect")
    else:
        return abort(401, "The verification code is not correct")
