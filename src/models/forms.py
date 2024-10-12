
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length

from src.models.user import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])

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
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Log In")


class newQuestionform(FlaskForm):
    question = StringField("Question", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    answer = StringField("Answer", validators=[DataRequired()])
    score = StringField("Score", validators=[DataRequired()])
    difficulty = StringField("Difficulty", validators=[DataRequired()])

    def validate_answer(self, answer):
        if answer.data not in [self.option1.data, self.option2.data, self.option3.data, self.option4.data]:
            raise ValidationError("Answer must be one of the options")


class newQuizform(FlaskForm):
    quiz_name = StringField("Quiz Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    time_limit = StringField("Time Limit", validators=[DataRequired()])
    questions = FieldList(FormField(newQuestionform), min_entries=1)

    submit = SubmitField("Create Quiz")
    add_question = SubmitField("Add Question")


class solveQuizForm(FlaskForm):
    answers = FieldList(StringField("Answer", validators=[DataRequired()]))
    submit = SubmitField("Submit Answers")
    next_question = SubmitField("Next Question")
    previous_question = SubmitField("Previous Question")
    submit_quiz = SubmitField("Submit Quiz")
