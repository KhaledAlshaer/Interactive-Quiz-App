from flask import Flask, flash, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash
from models.user import User

app = Flask(__name__)

@app.route("/register", methods = ["GET", "POST"])
def register():
    """
    Handle user registration.
    - Display a registration form for new users.
    - Collect user details (username, password, etc.).
    - Validate and save the user to the database.
    - Redirect to login page or show success message after successful registration.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        User.add(User(username, password, email))

        flash("Registration successful! Please log in.")
        return redirect(url_for("log_in"))
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def log_in():
    """
    Handle user login.
    - Display login form for existing users.
    - Verify the entered username and hashed password against the database.
    - Create a user session on successful login.
    - Redirect to the user's profile or the main dashboard after login.
    """
    if request.method == "POST":
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/profile")
def profile():
    """
    Display the user's profile.
    - Fetch and display user-specific information (username, quizzes taken, total score, etc.).
    - Allow users to update their personal details or view their quiz history.
    """
    return "hi"

@app.route("/quizzes/<quiz_id>")
def quiz(quiz_id):
    """
    Display the quiz page.
    - Fetch the quiz details based on quiz_id.
    - Display the questions and answer options.
    - Track the user's progress and responses.
    """
    return "hi"

@app.route("/results/<quiz_id>")
def results(quiz_id):
    """
    Display the quiz results.
    - Fetch the user's answers and compare them with the correct answers.
    - Calculate the score and show the result (e.g., correct answers, total score).
    - Provide feedback on each question (e.g., correct/incorrect).
    """
    return "hi"

@app.route("/submit_quiz/<quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    """
    Handle quiz submission.
    - Accept the user's answers via POST request.
    - Validate the answers and calculate the score.
    - Save the user's results in the database.
    - Redirect to the results page or show a success message.
    """
    return "hi"

@app.route("/logout")
def log_out():
    """
    Log out the user.
    - Clear the user session and log them out.
    - Redirect to the login page or home page.
    """
    return "hi"