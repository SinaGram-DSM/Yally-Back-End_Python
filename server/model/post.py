from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text

from server.model import Base


class Post(Base):
    __tablename__ = 'posts'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(String(40), nullable=False, primary_key=True)
    content = Column(String(100), nullable=True)
    img = Column(String(40), nullable=True)
    sound = Column(String(40), nullable=False)
    userEmail = Column(ForeignKey('users.email'), nullable=False)
    createdAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))



