
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


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
    quiz = relationship('Quiz', back_populates='questions')
    text = Column(String(255), nullable=False)
    choices = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False)
    category = Column(String(255), nullable=False)
    difficulty = Column(String(255), nullable=False)

    def __init__(self, text: str, choices: list,
                 correct_answer: str, score: int, category: str, difficulty: str, quiz):
        """
        Initialize a new Question object.
        """
        if correct_answer not in choices:
            raise ValueError("Correct answer must be one of the choices.")

        self.text = text
        self.choices = choices
        self.correct_answer = correct_answer
        self.score = score
        self.category = category
        self.difficulty = difficulty
        self.quiz = quiz

    def is_correct(self, answer: str) -> bool:
        """
        Check if the provided answer matches the correct answer.
        """
        return answer == self.correct_answer
