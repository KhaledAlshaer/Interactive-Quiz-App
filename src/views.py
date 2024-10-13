from flask import flash, jsonify, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash

from src.models import quiz
from src.models.quiz import Quiz

from .models.user import User
from .models.forms import RegistrationForm, LoginForm, newQuestionform, newQuizform, solveQuizForm
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
        password = generate_password_hash(form.password.data)
        email = form.email.data
        User.add(User(username, password, email))

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
        if user and user.authenticate(password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(url_for(next_page)) if next_page else redirect(url_for("profile"))
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
            quiz.questions = []

            for question_form in form.questions:
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