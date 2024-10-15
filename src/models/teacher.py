import bcrypt
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from user import User


class Teacher(User):
    """
    """
    quizzes = relationship("Quiz", back_populates="teacher")

    def __init__(self, Username: str, Password: str, email: str, is_admin: bool = True):
        super().__init__(Username, Password, email, is_admin)