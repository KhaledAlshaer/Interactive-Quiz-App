

from src.models.users_quizzes import UserQuiz
from add_mock_data import mock_data
from src.models.user import User
from src.models.users_quizzes import UserQuiz
from src.models.quiz import Quiz
from src.models import db
db.drop_tables()
db.create_tables()
mock_data.mock_users()
mock_data.mock_quizes()

# UserQuiz.add_by_ids(50, 1, 386)
# UserQuiz.add_by_ids(50, 5, 200)
# UserQuiz.add_by_ids(50, 9, 100)
