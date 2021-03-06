from flask import Flask, current_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from server import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES


def create_app():
    _app = Flask(__name__, instance_relative_config=True)

    CORS(_app)

    class CustomApi(Api):
        def handle_error(self, e):
            for val in current_app.error_handler_spec.values():
                for handler in val.values():
                    registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                    if len(registered_error_handlers) > 0:
                        raise e
            return super().handle_error(e)

    api = CustomApi(_app)

    _app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES

    JWTManager(_app)

    from server.view.ping import Ping
    api.add_resource(Ping, "/ping")

    from server.view.user import User
    api.add_resource(User, "/user")

    from server.view.user import Auth
    api.add_resource(Auth, "/user/auth")

    from server.view.user import Refresh
    api.add_resource(Refresh, "/user/auth/refresh")

    from server.view.user import CheckAuthCode
    api.add_resource(CheckAuthCode, "/user/auth-code")

    from server.view.user import SendAuthEmail
    api.add_resource(SendAuthEmail, "/user/auth-code/email")

    from server.view.user import SendResetEmail
    api.add_resource(SendResetEmail, "/user/reset-code/email")

    from server.view.user import ChangePassword
    api.add_resource(ChangePassword, "/user/auth/password")

    from server.view.profile import GetProfileTimeline
    api.add_resource(GetProfileTimeline, "/mypage/timeline/<email>/<page>")

    from server.view.listen import Listen
    api.add_resource(Listen, "/user/listening/<email>")

    from server.view.search import GetUserSearch
    api.add_resource(GetUserSearch, "/search/user")

    return _app
