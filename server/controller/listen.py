from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from server.model import session
from server.model.listen import Listen
from server.model.user import User


def listening(owner_email, listening_email):

    if owner_email == listening_email:
        return abort(400, "자기 자신을 리슨할 수는 없어요")

    listening_state = session.query(Listen).\
                        filter(Listen.listeningEmail == listening_email).\
                        filter(Listen.listenerEmail == owner_email).first()

    if listening_state:
        return abort(400, "이미 리슨 하고 있어요")

    listening_user = session.query(User).filter(User.email == listening_email).first()

    if listening_user:
        try:
            new_listening = Listen(listeningEmail=listening_email, listenerEmail=owner_email)

            session.add(new_listening)
            session.commit()

            return {
                "message": "Success"
            }

        except SQLAlchemyError:
            return abort(500, "db_error")

    else:
        return abort(404, "No such user")


def unlistening(owner_email, listening_email):

    if owner_email == listening_email:
        return abort(400, "자기 자신을 언리슨할 수는 없어요")

    listening_state = session.query(Listen). \
        filter(Listen.listeningEmail == listening_email). \
        filter(Listen.listenerEmail == owner_email).first()

    if listening_state is None:
        return abort(400, "이미 리슨 하지 않고 있어요")

    listening_user = session.query(User).filter(User.email == listening_email).first()

    if listening_user:

        try:
            session.delete(listening_state)

            session.commit()

            return {
                "message": "Success"
            }

        except SQLAlchemyError:
            return abort(500, "db_error")
    else:
        return abort(404, "No such user")



