from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/register")
def register():
    """
    Handle user registration.
    - Display a registration form for new users.
    - Collect user details (username, password, etc.).
    - Validate and save the user to the database.
    - Redirect to login page or show success message after successful registration.
    """

    return "hi"


@app.route("/login")
def login():
    """
    Handle user login.
    - Display login form for existing users.
    - Verify the entered username and hashed password against the database.
    - Create a user session on successful login.
    - Redirect to the user's profile or the main dashboard after login.
    """
    return "hi"


@app.route("/logout")
def logout():
    """
    Log out the user.
    - Clear the user session and log them out.
    - Redirect to the login page or home page.
    """
    return "hi"


@app.route("/profile")
def profile():
    """
    Display the user's profile.
    - Fetch and display user-specific information (username, quizzes taken, total score, etc.).
    - Allow users to update their personal details or view their quiz history.
    """
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








if __name__ == "__main__":
    app.run(debug=True)
