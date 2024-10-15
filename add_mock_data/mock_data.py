
from random import randint


def mock_users():
    from src.models.user import User

    try:
        user = User("Ahmed Arafa", "303", "admin1@gmail.com", 8888, is_admin=True)
        User.add(user)
        user = User("Khaled Alshaer", "4444", "admin2@gmail.com", 9999, is_admin=True)
        User.add(user)
    except Exception as e:
        pass
    for i in range(1, 50):
        user = User(f"User {i}", f"pass{randint(100,9999)}",
                    f"{i}@gmail.com", randint(0, 1000))
        User.add(user)


def mock_quizes():
    from src.models.quiz import Quiz
    from src.models.question import Question
    difficulties = ["Easy", "Medium", "Hard"]
    choices = ["A", "B", "C", "D"]
    for i in range(1, 35):
        quiz = Quiz(f"Quiz {i}",
                    "General Knowledge", randint(1, 60))
        for j in range(1, randint(2, 100)):
            # When creating a new Question and linking it to a Quiz,
            # it will automatically be added to quiz.questions.
            # Therefore, there is no need to call quiz.add_question,
            # as it would result in adding the question twice.
            quiz.add_question(f"Question {j}", choices, "A", randint(
                1, 10), difficulties[randint(0, 2)])
        Quiz.add(quiz)
