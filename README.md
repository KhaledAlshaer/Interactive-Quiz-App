# Interactive Quiz Application

## Overview

The **Interactive Quiz Application** is a web-based platform that provides users with a fun and interactive way to test their knowledge on various topics. Users can register, log in, and take quizzes, track their scores, and view quiz results. Teachers can manage quizzes, including creating, editing, and deleting quizzes.

## Key Features

- **User Registration & Authentication**: Secure user registration and login using hashed passwords and session management via `flask-login`.
- **Quiz Participation**: Users can take quizzes, see their scores immediately, and review the correct answers after completion.
- **Quiz Management for Teachers**: Teachers can create, edit, and delete quizzes, manage questions, and track students' progress.
- **Score Tracking**: The system allows users to track their progress over multiple quiz attempts.
- **Responsive Design**: The application is optimized for all screen sizes, providing a smooth experience on desktops, tablets, and mobile devices.

## Technologies

- **Backend**: Python, Flask
- **Frontend**: HTML, Flask-WTForms
- **Database**: MySQL, SQLAlchemy ORM
- **Security**: Flask-Bcrypt for password hashing, CSRF protection via Flask-WTF
- **Login Management**: Flask-Login for user session management

## Setup and Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/Interactive-Quiz-App.git
```

### 2. Navigate to the project directory:

```bash
cd Interactive-Quiz-App
```

### 3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up the database:

- Configure your database connection in `src/models/__init__.py`:

```python
    db = DB("mysql+mysqlconnector://root:303@localhost/quiz") // defult
    db = DB("mysql+mysqlconnector://<user>:<password>@localhost/<database_name>") // defult
```

### 5. Run the application:

```bash
python run.py
```

## Usage

- **Register**: Sign up for a new account using the registration page.
- **Login**: Access your account using your registered credentials.
- **Participate in Quizzes**: Start answering questions from available quizzes.
- **Score & Review**: View your score after completing a quiz and track your progress over time.
- **Teacher Features**: If registered as a teacher, you can add, edit, or delete quizzes and track the progress of your students.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch with your feature or bug fix.
3. Submit a pull request to the main repository.

Please ensure your code follows best practices and includes sufficient documentation and test cases.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributors

- Khaled Alshaer
- Ahmed Arafa
