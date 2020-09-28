from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager


def create_app():
    _app = Flask(__name__)

    api = Api(_app)

    from server.view.ping import Ping
    api.add_resource(Ping, "/ping")

    from server.view.user import User
    api.add_resource(User, "/user")

    return _app
