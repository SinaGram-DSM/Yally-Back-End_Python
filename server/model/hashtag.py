from sqlalchemy import Column, String, ForeignKey

from server.model import Base


class Hashtag(Base):
    __tablename__ = 'hastags'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    postId = Column(ForeignKey('posts.id', onupdate="cascade", ondelete="cascade"), nullable=False)
    content = Column(String(20), nullable=False)