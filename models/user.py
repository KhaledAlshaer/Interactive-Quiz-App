import hashlib
from .base import Base
from .db import db
from sqlalchemy import Column, Integer, String


class User(Base):
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
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Score = Column(Integer, default=0)

    def __init__(self, Username: str, Password: str, Score: int = 0):
        self.Username = Username
        self.Password = self.hash_password(Password)

        self.Score = Score

    def hash_password(self, Password: str) -> str:
        """
        Hash the password for secure storage.
        """
        return hashlib.sha256(Password.encode()).hexdigest()

    def authenticate(self, Password: str):
        """
        Authenticate the user by comparing the given password's hash 
        with the stored hashed password.
        """
        return self.Password == self.hash_password(Password)

    def update_score(self, new_score: int):
        """
        Update the user's total score.
        """
        self.Score += new_score

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

    @staticmethod
    def add(user: 'User'):
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
            print(e)

    @staticmethod
    def get_user(username: str) -> 'User':
        """
        Retrieve a user from the database by username.
        """
        return db.session.query(User).filter_by(Username=username).first()

    @staticmethod
    def update(user: 'User'):
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
                db.session.merge(user)
                db.session.commit()
            else:
                raise ValueError("User does not exist.")

        except Exception as e:
            db.session.rollback()
            print(e)

    @staticmethod
    def delete(user: 'User'):
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
            print(e)
