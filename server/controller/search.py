from sqlalchemy.exc import SQLAlchemyError
from flask import abort

from server.model import session
from server.model.user import User
from server.model.listen import Listen


def get_user_search_info(owner_email, user_nickname):
    try:
        user = session.query(User).filter(User.nickname.like(f"{user_nickname}%")).all()
    except SQLAlchemyError:
        return abort(418, "db_error")

    return {
        "users": [{
            "email": user_info.email,
            "img": user_info.img,
            "nickname": user_info.nickname,
            "listening": session.query(Listen).filter(Listen.listeningEmail == user_info.email).count(),
            "listener": session.query(Listen).filter(Listen.listenerEmail == user_info.email).count(),
            "isListening": True if session.query(Listen).filter(Listen.listenerEmail == owner_email).filter(Listen.listeningEmail == user_info.email).first() else False
        }for user_info in user]
    }
