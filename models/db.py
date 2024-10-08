
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from .base import Base


class DB:
    def __init__(self, db_url: str = "mysql+mysqlconnector://root:303@localhost/quiz"):
        self.engine = create_engine(db_url)
        self.__session = None

    @property
    def session(self) -> Session:
        if not self.__session:
            session = sessionmaker(bind=self.engine)
            self.__session = session()
        return self.__session

    @staticmethod
    def create_tables():
        Base.metadata.create_all(db.engine, checkfirst=True)

    @staticmethod
    def drop_tables():
        Base.metadata.drop_all(db.engine)


db = DB()
db.create_tables()
