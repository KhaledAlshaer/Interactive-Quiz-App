from flask import flash, jsonify, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash

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
def logout():
    """
    Log out the user.
    - Clear the user session and log them out.
    - Redirect to the login page or home page.
    """
    logout_user()
    return redirect(url_for("log_in"))


@app.route("/profile")
def profile():
    """
    Display the user's profile.
    - Fetch and display user-specific information (username, quizzes taken, total score, etc.).
    - Allow users to update their personal details or view their quiz history.
    """
    # username
    # email
    # id
    # quizz
    # score

    return "hi"


@app.route("/quizzes")
def quizzes():
    from models.quiz import Quiz
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """

    all_quizzes = [quiz.to_dict() for quiz in Quiz.get_all_quizzes()]
    return jsonify(all_quizzes), 200


@app.route("/quiz/<quiz_id>")
def quiz(quiz_id):
    from models.quiz import Quiz
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """
    quiz = Quiz.get_quiz_by_id(quiz_id)
    return jsonify(quiz.to_dict()), 200
