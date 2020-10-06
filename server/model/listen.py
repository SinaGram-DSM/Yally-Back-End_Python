from sqlalchemy import Column, String, ForeignKey

from server.model import Base


class Listen(Base):
    __tablename__ = 'listens'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    listenerEmail = Column(ForeignKey('users.email'), primary_key=True)
    listeningEmail = Column(ForeignKey('users.email'), primary_key=True)

