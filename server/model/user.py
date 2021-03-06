from sqlalchemy import Column, String, INT

from server.model import Base


class User(Base):
    __tablename__ = 'users'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    email = Column(String(30), primary_key=True)
    password = Column(String(100), nullable=False)
    nickname = Column(String(20), nullable=False)
    age = Column(INT, nullable=False)
    img = Column(String, nullable=True, default='user.jpg')
