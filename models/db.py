from requests import session
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
            Session = sessionmaker(bind=self.engine)
            self.__session = Session()
        return self.__session

    def create_tables(self):
        Base.metadata.create_all(self.engine, checkfirst=True)


db = DB()
db.create_tables()
