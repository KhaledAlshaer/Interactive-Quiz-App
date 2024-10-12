from flask import Flask


app = Flask(__name__)
app.secret_key = "2e12d23e-783a-4430-82ad-5c2f6713b4a4"

from src import views