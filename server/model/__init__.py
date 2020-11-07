import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from server import DATABASE_URL
engine = create_engine(DATABASE_URL, encoding="utf-8", pool_size=20,
                       pool_recycle=3600, max_overflow=20, pool_pre_ping=True)

Base = declarative_base()

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
