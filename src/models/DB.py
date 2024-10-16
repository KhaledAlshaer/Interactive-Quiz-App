
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from .base import Base


class DB:

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.__session = None

    @property
    def session(self) -> Session:
        if not self.__session:
            session = sessionmaker(bind=self.engine)
            self.__session = session()
        return self.__session

    @classmethod
    def create_tables(cls):
        from src.models import db
        Base.metadata.create_all(db.engine, checkfirst=True)

    @classmethod
    def drop_tables(cls):
        from src.models import db
        Base.metadata.drop_all(db.engine)


# db = DB()
# DB.create_tables()
