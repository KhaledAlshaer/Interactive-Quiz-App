
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, ValidationError, FieldList, FormField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from src import app
from src.models.quiz import Quiz
from src.models.user import User
csrf = CSRFProtect(app)


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=2, max=16)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    is_teacher = BooleanField("Are you a teacher?")

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.get_user_by_username(username.data)
        if user:
            raise ValidationError(
                "Username already exists. Please choose a different one.")

    def validate_email(self, email):
        user = User.get_user_by_email(email.data)
        if user:
            raise ValidationError(
                "Email already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=2, max=16)])
    submit = SubmitField("Log In")


class newQuestionform(FlaskForm):
    question = StringField("Question", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    answer = StringField("Answer", validators=[DataRequired()])
    score = IntegerField("Score", validators=[DataRequired()])
    difficulty = StringField("Difficulty", validators=[DataRequired()])

    def validate_answer(self, answer):
        if answer.data not in [self.option1.data, self.option2.data, self.option3.data, self.option4.data]:
            raise ValidationError("Answer must be one of the options")


class newQuizform(FlaskForm):
    from src.models.quiz import Quiz
    quiz_name = StringField("Quiz Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    time_limit = IntegerField("Time Limit", validators=[DataRequired()])
    questions = FieldList(FormField(newQuestionform), min_entries=1)

    submit = SubmitField("Create Quiz")
    add_question = SubmitField("Add Question")

    def fill(self, quiz: Quiz):
        self.quiz_name.data = quiz.name  # type: ignore
        self.category.data = quiz.quiz_category  # type: ignore
        self.time_limit.data = quiz.time_limit  # type: ignore
        while len(self.questions) < len(quiz.questions):
            self.questions.append_entry()
        for i, question in enumerate(quiz.questions):
            self.questions[i].question.data = question.text
            self.questions[i].option1.data = question.choices[0]
            self.questions[i].option2.data = question.choices[1]
            self.questions[i].option3.data = question.choices[2]
            self.questions[i].option4.data = question.choices[3]
            self.questions[i].answer.data = question.correct_answer
            self.questions[i].score.data = question.score
            self.questions[i].difficulty.data = question.difficulty


class solveQuizForm(FlaskForm):
    answers = FieldList(SelectField("answer", validators=[
                        DataRequired()]), min_entries=1)
    submit = SubmitField("Submit Quiz")

    def fill(self, quiz: Quiz):
        while len(self.answers) < len(quiz.questions):
            self.answers.append_entry()

        for question, answer in zip(quiz.questions, self.answers):
            choices = [""] + question.choices
            answer.choices = choices
