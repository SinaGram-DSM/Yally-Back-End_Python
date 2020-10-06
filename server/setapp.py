from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from server import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES


def create_app():
    _app = Flask(__name__)

    CORS(_app)

    api = Api(_app)

    _app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    jwt = JWTManager(_app)

    from server.view.ping import Ping
    api.add_resource(Ping, "/ping")

    from server.view.user import User
    api.add_resource(User, "/user")

    from server.view.user import Auth
    api.add_resource(Auth, "/user/auth")

    from server.view.user import Refresh
    api.add_resource(Refresh, "/user/auth/refresh")

    from server.view.user import SendMail
    api.add_resource(SendMail, "/user/auth-code/email")

    from server.view.listen import Listen
    api.add_resource(Listen, "/user/listening")

    return _app
