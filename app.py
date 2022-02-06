from flask import Flask
from routes import wordle


# Create Flask's `app` object
app = Flask(__name__, template_folder="templates")
app.register_blueprint(wordle)
