from question import Question

class Quiz:
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

    def __init__(self, quiz_id: int, number_of_questions: int,
                total_score: int, quiz_category: str, time_limit: int):
        """
        Initialize a new Quiz object.
        """
        self.quiz_id = quiz_id
        self.questions = []
        self.number_of_questions = number_of_questions
        self.total_score = total_score
        self.quiz_category = quiz_category
        self.time_limit = time_limit

    def add_question(self, question: Question):
        """
        Add a question to the quiz.

        Args:
        - question (Question): A Question object to add to the quiz.
        
        Raises:
        - TypeError: If the argument is not an instance of the Question class.
        """
        if not isinstance(question, Question):
            raise TypeError("The argument must be an instance of the Question class.")
        
        self.questions.append(question)

    def calculate_total_score(self):
        """
        Calculate the total possible score for the quiz by summing 
        the scores of all the questions.
        """
        self.total_score = sum(question.score for question in self.questions)

    def get_question_by_id(self, question_id: int):
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
