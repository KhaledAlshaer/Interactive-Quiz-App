import traceback
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.models import db


from .base import Base


class UserQuiz(Base):

    """
    This class represents the association between users and quizzes,
    including the score for each user in each quiz.
    """
    __tablename__ = 'users_quizzes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.ID'))
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))

    @classmethod
    def add(cls, user, quiz, score: int):
        """
        Add a new user-quiz association to the database.
        """
        from models.user import User
        from models.quiz import Quiz
        if not isinstance(user, User):
            raise TypeError(
                "The user argument must be an instance of the User class.")
        if not isinstance(quiz, Quiz):
            raise TypeError(
                "The quiz argument must be an instance of the Quiz class.")
        if score < 0 or score > quiz.total_score:  # type: ignore
            raise ValueError(
                "The score must be between 0 and the total score of the quiz.")

    @classmethod
    def add_by_ids(cls, user_id, quiz_id, score: int):
        """
        Add a new user-quiz association to the database using user and quiz IDs.
        """
        from src.models.user import User
        user_quiz = UserQuiz(user_id=user_id, quiz_id=quiz_id, score=score)
        try:
            db.session.add(user_quiz)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)
        finally:
            user = User.get_user_by_id(user_id)
            user.update_score()
            User.update(user)
