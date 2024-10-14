from operator import is_
import traceback
import bcrypt
from tomlkit import boolean
from werkzeug.security import generate_password_hash, check_password_hash
from .base import Base
from src.models import db

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from src import login_manager
from bcrypt import hashpw, checkpw 


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(int(user_id))


class User(Base, UserMixin):
    from .users_quizzes import UserQuiz

    """
    This class represents a user in the Interactive Quiz Application.

    Attributes:
    1. username (str): The username chosen by the user, used for login.
    2. password (str): The hashed password of the user for security.
    3. ID (int): A unique identifier for each user in the system.
    4. score (int): The user's total score or points accumulated from quiz attempts.

    Methods:
    1. authenticate(password: str): Validates the user's password.
    2. update_score(new_score: int): Updates the user's total score based on quiz results.
    3. reset_password(new_password: str): Allows the user to reset their password.
    4. get_user_info(): Returns the user's information, excluding sensitive data like the password.
    """
    __tablename__ = 'users'
    Username = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Score = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)
    quizzes = relationship(
        "Quiz",  secondary="users_quizzes", back_populates="users", lazy='dynamic')

    def __init__(self, Username: str, Password: str, email: str, Score: int = 0, is_admin: bool = False):
        self.Username = Username
        self.Password = self.hash_password(Password)
        self.email = email
        self.is_admin = is_admin

    def hash_password(self, Password: str) -> str:
        """
        Hash the password for secure storage.
        """
        hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return hashed_password

    def is_password(self, Password: str) -> bool:
        """
        Authenticate the user by comparing the given password with the stored hashed password.
        """
        return bcrypt.checkpw(Password.encode('utf-8'), self.Password.encode('utf-8'))

    def update_score(self):
        """
        Update the user's total score.
        """
        from src.models.users_quizzes import UserQuiz
        self.Score += sum([userquiz.score for userquiz in db.session.query(
            UserQuiz).filter_by(user_id=self.ID).all()])

    def reset_password(self, new_password: str):
        """
        Reset the user's password with a new hashed password.
        """
        self.Password = self.hash_password(new_password)

    def get_user_info(self):
        """
        Get user's information, excluding sensitive data like password.
        """
        return {
            "username: ": self.Username,
            "ID: ": self.ID,
            "score: ": self.Score
        }

    def __repr__(self) -> str:
        """
        Return a string representation of the user object.
        """
        return f"User(username={self.Username}, ID={self.ID}, Score={self.Score})"

    def get_id(self):
        return self.ID

    @classmethod
    def add(cls, user: 'User'):
        """
        Add a user to the database.
        """
        if not isinstance(user, User):
            raise TypeError(
                "The argument must be an instance of the User class.")
        if user is None:
            raise ValueError("User is None.")
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)

    @classmethod
    def get_user_by_username(cls, username: str) -> 'User':
        """
        Retrieve a user from the database by username.
        """
        return db.session.query(User).filter_by(Username=username).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> 'User':
        """
        Retrieve a user from the database by username.
        """
        return db.session.query(User).filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, id: int) -> 'User':
        """
        Retrieve a user from the database by username.
        """
        return db.session.query(User).filter_by(ID=id).first()

    @classmethod
    def update(cls, user: 'User'):
        """
        Update a user in the database.
        """
        if not isinstance(user, User):
            raise TypeError(
                "The argument must be an instance of the User class.")
        if user is None:
            raise ValueError("User is None.")
        try:
            is_user = db.session.query(User).filter_by(ID=user.ID).first()
            if is_user:
                # user.update_score()
                db.session.merge(user)
                db.session.commit()
            else:
                raise ValueError("User does not exist.")

        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)

    @classmethod
    def delete(cls, user: 'User'):
        """
        Delete a user from the database.
        """
        if not isinstance(user, User):
            raise TypeError(
                "The argument must be an instance of the User class.")
        if user is None:
            raise ValueError("User is None.")
        try:
            is_user = db.session.query(User).filter_by(ID=user.ID).first()
            if is_user:
                db.session.delete(user)
                db.session.commit()
            else:
                raise ValueError("User does not exist.")

        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)
