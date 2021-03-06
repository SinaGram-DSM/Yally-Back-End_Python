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

    pre_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NumberEmail</title>
            <style>
                body{
                    position: relative;
                    height: 90vh;
                    width: 50%;
                    margin: 0;
                }
                .background{
                    width: 100%;
                    position: absolute;
                    bottom: 10%;
                }
                #container{
                    display: flex;
                    justify-content: center;
                    padding-top: 100px;
                }
                p{
                    text-align: center;
                }
                .logoImg
                {
                    width: 290px;
                    height: 230px;
                }
            </style>
        </head>
        <body>
            <div id='container'>
                <div>
                    <img src="../../assets/img/logo-purple.png" class="logoImg">
                    <p>
                    
        """

    postfix_html = """
                    </p>
                    <p>얄리에서 더 넓은 세상을 들어보세요.</p>
                </div>
            </div>
            <img class="background" src="../../assets/img/background.png">

        </body>
        </html>
        """

    html_body = pre_html + str(code) + postfix_html

    try:
        save_code_into_redis(email, code, codetype=codetype)

    except ConnectionError:
        abort(418, "redis_error")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASSWORD)

    msg = MIMEText(html_body, 'html')
    msg['Subject'] = f"yally {codetype} code"

    server.sendmail(EMAIL_ID, email, msg.as_string())
    server.quit()

    return


def send_auth_code_email(email):

    send_code_to_email(email, codetype="auth")

    return {
        "message": "Successfully send auth code"
    }


def send_reset_code_email(email):

    send_code_to_email(email, codetype="reset")

    return {
        "message": "Successfully send reset code"
    }


def send_email(email, codetype):
    user = session.query(User).filter(User.email == email).first()

    if codetype == 'auth':
        if user:
            return abort(409, "This email is already sign up")

        return send_auth_code_email(email)

    elif codetype == 'reset':
        if user:
            return send_reset_code_email(email)

        return abort(404, "User not found")


# check_code 하나로 만들기 + 기능분리
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
