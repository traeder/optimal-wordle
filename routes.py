from flask import render_template, Blueprint, request
wordle = Blueprint('wordle', __name__, template_folder="templates")



@wordle.route('/')
def home():
    """Landing page."""
    return render_template(
        'home.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja."
    )

@wordle.route('/guess', methods=['POST'])
def optimal_guess():
    request_data = request.form
    