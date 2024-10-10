
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
    for i in range(1, 1000):
        quiz = Quiz(f"Quiz {i}", randint(0, 100),
                    "General Knowledge", randint(1, 60))
        for j in range(randint(1, 100)):
            quiz.add_question(
                Question(f"Question {j}", ["A", "B", "C", "D"], "A", randint(1, 10), "General Knowledge", difficulties[randint(0, 2)], quiz))
        Quiz.add(quiz)
