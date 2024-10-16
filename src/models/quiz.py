import traceback
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .question import Question

from sqlalchemy.orm import relationship
from .base import Base
from src.models import db


class Quiz(Base):
    from src.models.users_quizzes import UserQuiz
    from src.models.user import User
    """
     This class represents a quiz made up of multiple questions.

    Attributes:
    - quiz_id (int): A unique identifier for the quiz.
    - questions (list): A list of Question objects in the quiz.
    - number_of_questions (int): Total number of questions in the quiz.
    - total_score (int): Total possible score for the quiz.
    - quiz_category (str): The category of the quiz (e.g., Math, Science).
    - time_limit (int): Time limit for completing the quiz (in minutes).
    """
    __tablename__ = 'quizzes'
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    total_score = Column(Integer, nullable=False)
    quiz_category = Column(String(255), nullable=False)
    time_limit = Column(Integer, nullable=False)
    questions = relationship(
        "Question", back_populates='quiz', cascade="all, delete-orphan")
    users = relationship("User",  secondary="users_quizzes",
                         back_populates="quizzes", lazy="joined")
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __init__(self, name: str, quiz_category: str, time_limit: int):
        """
        Initialize a new Quiz object.
        """

        self.name = name
        self.total_score = 0
        self.quiz_category = quiz_category
        self.time_limit = time_limit

    @property
    def number_of_questions(self):
        """
        Return the total number of questions in the quiz.
        """
        return len(self.questions)

    def add_question(self, text: str, choices: list,
                     correct_answer: str, score: int, difficulty: str):
        """
        Add a question to the quiz.

        Args:
        - question (Question): A Question object to add to the quiz.

        Raises:
        - TypeError: If the argument is not an instance of the Question class.
        """
        db.session.add(Question(text, choices, correct_answer,
                                score, difficulty, self))
    # def add_questions(self, questions: list):
    #     """
    #     Add a question to the quiz.

    #     Args:
    #     - question (Question): A Question object to add to the quiz.

    #     Raises:
    #     - TypeError: If the argument is not an instance of the Question class.
    #     """
    #     for question in questions:
    #         if not isinstance(question, Question):
    #             raise TypeError(
    #                 "The argument must be an instance of the Question class.")
    #         self.add_question(question)

    def calculate_total_score(self):
        """
        Calculate the total possible score for the quiz by summing
        the scores of all the questions.
        """
        self.total_score = sum([question.score for question in self.questions])

    def get_question_by_id(self, question_id: int) -> Question:
        """
         Retrieve a question from the quiz by its question_id.

        Args:
        - question_id (int): The unique ID of the question to retrieve.

        Returns:
        - Question: The Question object with the matching ID.

        Raises:
        - ValueError: If no question with the given ID is found.
        """
        for question in self.questions:
            if question.question_id == question_id:
                return question
        raise ValueError(f"Question with ID {question_id} not found.")

    def __str__(self):
        return f"Quiz: {self.name}, Category: {self.quiz_category}, Number of Questions: {self.number_of_questions}, Total Score: {self.total_score}, Time Limit: {self.time_limit} minutes."

    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "name": self.name,
            "questions": [question.to_dict() for question in self.questions],
            "total_score": self.total_score,
            "quiz_category": self.quiz_category,
            "time_limit": self.time_limit
        }

    @classmethod
    def add(cls, quiz: 'Quiz'):
        """
        Add a quiz to the database.
        """
        if not isinstance(quiz, Quiz):
            raise TypeError(
                "The argument must be an instance of the Quiz class.")
        if quiz is None:
            raise ValueError("Quiz is None.")
        try:
            quiz.calculate_total_score()
            db.session.add(quiz)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)

    @classmethod
    def get_quiz_by_name(cls, name: str) -> 'Quiz':
        """
        Retrieve a quiz from the database by name.
        """
        return db.session.query(Quiz).filter_by(name=name).first()  # type: ignore

    @classmethod
    def get_quiz_by_id(cls, id: int) -> 'Quiz':
        """
        Retrieve a quiz from the database by name.
        """
        return db.session.query(Quiz).filter_by(quiz_id=id).first()

    @classmethod
    def get_all_quizzes(cls) -> list:
        """
        Retrieve all quizzes from the database.
        """
        return db.session.query(Quiz).all()

    @classmethod
    def update(cls, quiz: 'Quiz'):
        """
        Update a quiz in the database.
        """
        if not isinstance(quiz, Quiz):
            raise TypeError(
                "The argument must be an instance of the Quiz class.")
        if quiz is None:
            raise ValueError("Quiz is None.")
        try:
            quiz.calculate_total_score()

            is_quiz = db.session.query(Quiz).filter_by(
                quiz_id=quiz.quiz_id).first()
            if is_quiz:
                db.session.merge(quiz)
                db.session.commit()
            else:
                raise ValueError("Quiz does not exist.")

        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)

    @classmethod
    def delete(cls, quiz: 'Quiz'):
        """
        Delete a quiz from the database.
        """
        if not isinstance(quiz, Quiz):
            raise TypeError(
                "The argument must be an instance of the Quiz class.")
        if quiz is None:
            raise ValueError("Quiz is None.")
        try:
            is_quiz = db.session.query(Quiz).filter_by(
                quiz_id=quiz.quiz_id).first()
            if is_quiz:
                # for question in quiz.questions:
                #     db.session.delete(question)
                db.session.delete(quiz)
                db.session.commit()
            else:
                raise ValueError("Quiz does not exist.")

        except Exception as e:
            db.session.rollback()
            tb = traceback.format_exc()
            print(tb)
