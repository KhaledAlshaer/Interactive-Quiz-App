class Question:
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

    def __init__(self, question_id: int, text: str, choices: list, 
                correct_answer: str, score: int, category: str, difficulty: str):
        """
        Initialize a new Question object.
        """
        if correct_answer not in choices:
            raise ValueError("Correct answer must be one of the choices.")
            
        self.question_id = question_id
        self.text = text
        self.choices = choices
        self.correct_answer = correct_answer
        self.score = score
        self.category = category
        self.difficulty = difficulty

    def is_correct(self, answer: str) -> bool:
        """
        Check if the provided answer matches the correct answer.
        """
        return answer == self.correct_answer
