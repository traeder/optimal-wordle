import json, random

from flask import render_template, Blueprint, request
from words import Letters, WordProbability, load_letter_frequencies, load_word_list


wordle = Blueprint('wordle', __name__, template_folder="templates")
wp = WordProbability([load_letter_frequencies('english_monograms.txt'),
                      load_letter_frequencies('english_bigrams.txt'),
                      load_letter_frequencies('english_trigrams.txt')])
word_list = load_word_list('wordlist.txt')



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
    json_data = request.get_json(force=True)
    print(json_data)
    letters = Letters.from_wordle(json_data)
    print(letters.letters)
    valid_words = letters.filter_word_list(word_list)
    print(valid_words)
    best_words = wp.best_words_by_score(valid_words, 5)
    print(best_words)
    return json.dumps(best_words)

@wordle.route('/word', methods=['GET'])
@wordle.route('/word/<seed>', methods=['GET'])
def word(seed=None):
    subwords = [w for w in word_list if len(w) == 5]
    if seed is not None:
        random.seed(seed)
    ix = random.randint(0, len(subwords))
    return subwords[ix]