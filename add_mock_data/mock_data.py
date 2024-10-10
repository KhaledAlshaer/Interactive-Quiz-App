
from random import randint


def mock_users():
    from models.user import User

    try:
        user = User("Ahmed Arafa", "303", 8888)
        User.add(user)
        user = User("Khaled Alshaer", "4444", 9999)
        User.add(user)
    except Exception as e:
        pass
    for i in range(10, 1000):
        user = User(f"User {i}", f"pass{randint(100,9999)}", randint(0, 1000))
        User.add(user)


def mock_quizes():
    from models.quiz import Quiz
    from models.question import Question
    difficulties = ["Easy", "Medium", "Hard"]
    choices = ["A", "B", "C", "D"]
    for i in range(1, 10):
        quiz = Quiz(f"Quiz {i}",
                    "General Knowledge", randint(1, 60))
        for j in range(1, randint(2, 100)):
            # When creating a new Question and linking it to a Quiz,
            # it will automatically be added to quiz.questions.
            # Therefore, there is no need to call quiz.add_question,
            # as it would result in adding the question twice.
            quiz.add_question(f"Question {j}", choices, "A", randint(
                1, 10), "General Knowledge", difficulties[randint(0, 2)])
        Quiz.add(quiz)
