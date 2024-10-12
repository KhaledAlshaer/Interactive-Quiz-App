
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from src.models import db


class Question(Base):
    """
    This class represents a question in the quiz.

    Attributes:
    - question_id (int): A unique identifier for the question.
    - text (str): The question text.
    - choices (list): A list of possible answers (multiple-choice).
    - correct_answer (str): The correct answer from the choices.
    - score (int): Points awarded for a correct answer.
    - category (str): The category of the question (e.g., Math, Science).
    - difficulty (str): The difficulty level of the question (e.g., Easy, Medium, Hard).
    """
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True,
                         autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))
    quiz = relationship('Quiz', back_populates='questions',
                        )
    text = Column(String(255), nullable=False)
    choices = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False)
    
    difficulty = Column(String(255), nullable=False)

    def __init__(self, text: str, choices: list,
                 correct_answer: str, score: int, difficulty: str, quiz):
        """
        Initialize a new Question object.
        """
        if correct_answer not in choices:
            raise ValueError("Correct answer must be one of the choices.")

        self.text = text
        self.choices = choices
        self.correct_answer = correct_answer
        self.score = score
        
        self.difficulty = difficulty
        self.quiz = quiz
        self.quiz_id = quiz.quiz_id

    def is_correct(self, answer: str) -> bool:
        """
        Check if the provided answer matches the correct answer.
        """
        return answer == self.correct_answer

    def __str__(self):
        return f"{self.text} {self.choices} {self.correct_answer} {self.score} {self.category} {self.difficulty}"

    def to_dict(self):
        return {
            "text": self.text,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "score": self.score,
            "category": self.category,
            "difficulty": self.difficulty
        }

    # @classmethod
    # def add(question: 'Question'):
    #     """
    #     Add a new question to the database.
    #     """
    #     if not isinstance(question, Question):
    #         raise TypeError(
    #             "The argument must be an instance of the Question class.")
    #     if question is None:
    #         raise ValueError("The question cannot be None.")

    #     question.quiz.questions.append(question)

    #     Quiz.update(question.quiz)
