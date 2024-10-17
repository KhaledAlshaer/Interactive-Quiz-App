from flask import flash, jsonify, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash

from src.models import question, quiz
from src.models.quiz import Quiz
from src.models.users_quizzes import UserQuiz, UserQuestion

from src.models.user import User
from src.models.forms import RegistrationForm, LoginForm, newQuizform, solveQuizForm
from src import app, login_manager
from flask_login import login_user, login_required, current_user, logout_user
login_manager.login_view = "log_in"  # type: ignore


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration.
    - Display a registration form for new users.
    - Collect user details (username, password, etc.).
    - Validate and save the user to the database.
    - Redirect to login page or show success message after successful registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        is_teacher = form.is_teacher.data
        print(username, password)
        User.add(User(username, password, email, is_teacher=is_teacher))

        flash("Registration successful! Please log in.")
        return redirect(url_for("log_in"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def log_in():
    """
    Handle user login.
    - Display login form for existing users.
    - Verify the entered username and hashed password against the database.
    - Create a user session on successful login.
    - Redirect to the user's profile or the main dashboard after login.
    """
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.get_user_by_username(username)
        print(username, password, user)
        print(user.is_password(password))
        if user and user.is_password(password):
            login_user(user)

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("profile"))
        flash("Invalid username or password. Please try again.")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """
    Log out the user.
    - Clear the user session and log them out.
    - Redirect to the login page or home page.
    """
    logout_user()
    return redirect(url_for("log_in"))


@app.route("/profile")
@app.route("/")
@login_required
def profile():
    """
    Display the user's profile.
    - Fetch and display user-specific information (username, quizzes taken, total score, etc.).
    - Allow users to update their personal details or view their quiz history.
    """
    return render_template("profile.html", user=current_user, quiz_get_all=Quiz.get_all_quizzes())


@app.route("/quiz/add", methods=["GET", "POST"])
@login_required
def quiz_add():
    from src.models.quiz import Quiz
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """
    form = newQuizform()

    if form.validate_on_submit():
        if form.add_question.data:
            form.questions.append_entry()
        if form.submit.data:
            quiz = Quiz(form.quiz_name.data, form.category.data,
                        form.time_limit.data)

            for question_form in form.questions:
                quiz.add_question(question_form.question.data, [question_form.option1.data, question_form.option2.data, question_form.option3.data,
                                  question_form.option4.data], question_form.answer.data, question_form.score.data, question_form.difficulty.data)

            Quiz.add(quiz)
            if current_user.is_teacher:
                UserQuiz.add(current_user, quiz, 0)
            flash(f"Quiz {quiz.name} added successfully.")
            return redirect(url_for("profile"))
    return render_template("quiz_add.html", form=form)


@app.route("/quiz/edit/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz_edit(quiz_id: int):
    from .models.quiz import Quiz
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """
    form = newQuizform()
    quiz = Quiz.get_quiz_by_id(quiz_id)

    if form.validate_on_submit():
        if form.add_question.data:
            form.questions.append_entry()
        if form.submit.data:
            quiz.name = form.quiz_name.data
            quiz.quiz_category = form.category.data
            quiz.time_limit = form.time_limit.data

            for i, question_form in enumerate(form.questions):
                if i < len(quiz.questions):
                    quiz.questions[i].text = question_form.question.data
                    quiz.questions[i].choices = [question_form.option1.data, question_form.option2.data, question_form.option3.data,
                                                 question_form.option4.data]
                    quiz.questions[i].correct_answer = question_form.answer.data
                    quiz.questions[i].score = question_form.score.data
                    quiz.questions[i].difficulty = question_form.difficulty.data
                else:
                    quiz.add_question(question_form.question.data, [question_form.option1.data, question_form.option2.data, question_form.option3.data,
                        question_form.option4.data], question_form.answer.data, question_form.score.data, question_form.difficulty.data)

            Quiz.update(quiz)
            flash(f"Quiz {quiz.name} updated successfully.")
            return redirect(url_for("profile"))

    form.fill(quiz)
    form.submit.label.text = "Update Quiz"

    return render_template("quiz_edit.html", form=form)


@app.route("/quiz/delete/<int:quiz_id>", methods=["GET"])
@login_required
def quiz_delete(quiz_id: int):
    from .models.quiz import Quiz
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """

    quiz = Quiz.get_quiz_by_id(quiz_id)
    name = quiz.name
    Quiz.delete(quiz)
    flash(f"Quiz {name} deleted successfully.")
    return redirect(url_for("profile"))


@app.route("/quizzes")
@login_required
def quizzes():

    return render_template("quizzes.html", quizzes=Quiz.get_all_quizzes())


@app.route("/quiz/solve/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz_solve(quiz_id):
    """
Handle the quiz solving process for a given quiz ID.

This view function handles both GET and POST requests for solving a quiz.
It retrieves the quiz by its ID, populates the form with the quiz data,
and processes the form submission to calculate the user's score.

Args:
    quiz_id (int): The ID of the quiz to be solved.

Returns:
    Response: Renders the quiz solving template on GET request.
              Redirects to the profile page with a flash message on successful form submission.
"""
    form = solveQuizForm()
    quiz = Quiz.get_quiz_by_id(quiz_id)
    form.fill(quiz)
    if form.validate_on_submit():
        score = 0
        for i, question in enumerate(quiz.questions):
            UserQuestion.add(current_user.ID, quiz.quiz_id,
                             question.question_id, question.is_correct(
                                 form.answers[i].data))
            if question.is_correct(form.answers[i].data):
                score += question.score
        flash(f"Your score is {score}")
        UserQuiz.add(current_user, quiz, score)
        return redirect(url_for("profile"))
    return render_template("quiz_solve.html", form=form, questions=quiz.questions, quiz_name=quiz.name, zipped=zip(form.answers, quiz.questions), enumerate=enumerate)


@app.route("/quiz/result/<int:quiz_id>", methods=["GET"])
@login_required
def quiz_result(quiz_id):
    """
    Display the user's quiz results.
    - Fetch and display the user's quiz results (quizzes taken, scores, etc.).
    - Allow users to view their quiz history and performance.
    """
    quiz = Quiz.get_quiz_by_id(quiz_id)
    questions = []
    for question in quiz.questions:
        question_dict = {}
        question_dict = question.to_dict()
        question_dict["user_answer"] = UserQuestion.get_is_pass(
            current_user.ID, quiz_id, question.question_id)
        questions.append(question_dict)
    print(questions)
    return render_template("quiz_result.html", user=current_user, quiz=quiz, enumerate=enumerate, questions=questions)
