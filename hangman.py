'''
Program: Hangman

Last modification date: 4/5/23

Creator: Mihir Patel
'''

import random
from config import SECRET_KEY, DEBUG
from flask import Flask, render_template, request, redirect, url_for
from flask_redis import FlaskRedis
import json

hangman_app = Flask(__name__, static_folder='static', template_folder='static/templates')
hangman_app.config['SECRET_KEY'] = SECRET_KEY
hangman_app.config['DEBUG'] = DEBUG

hangman_app.config['SESSION_REDIS_URL'] = 'redis://localhost:6379/0'

redis_store = FlaskRedis(hangman_app)

words_to_guess = ["january","border","image","film","promise","kids","lungs","doll","rhyme","damage","plants"]

@hangman_app.route('/', methods=['GET', 'POST'])
def home_page_of_game():
    if request.method == 'POST':
        player_name = request.form['name']
        return redirect(url_for('play_game',player_name=player_name))

    return render_template('home.html')


@hangman_app.route('/inGame/<player_name>', methods=['GET', 'POST'])
def play_game(player_name):
    if not redis_store.get(player_name):
        word = random.choice(words_to_guess)
        player_info = {
            'word': word,
            'word_display': list('_' * len(word)),
            'guessed_letters': [],
            'correct_letters': [],
            'chances': 6
        }
        player_info_json = json.dumps(player_info)
        redis_store.set(player_name, player_info_json)

    else:
        player_info_json = redis_store.get(player_name)
        player_info = json.loads(player_info_json)
    
    word = player_info['word']
    word_display = player_info['word_display']
    guessed_letters = player_info['guessed_letters']
    correct_letters = player_info['correct_letters']
    chances = player_info['chances']

    if request.method == 'POST':
        letter = request.form['letter'].lower()
        if letter in guessed_letters or letter in correct_letters:
            return redirect(url_for('play_game',player_name=player_name))

        if letter in word:
            correct_letters.append(letter)
            for i in range(len(word)):
                if word[i] == letter and word_display[i] == '_':
                    word_display[i] = letter
        else:
            guessed_letters.append(letter)
            chances -= 1

        player_info['word_display'] = word_display
        player_info['guessed_letters'] = guessed_letters
        player_info['correct_letters'] = correct_letters
        player_info['chances'] = chances

        player_info_json = json.dumps(player_info)
        redis_store.set(player_name, player_info_json)


    if '_' not in word_display:
        return render_template('win.html', word=word, player_name=player_name)

    if chances == 0:
        return render_template('lose.html', word=word, player_name = player_name)

    remaining_letters = word_display.count('_')
    return render_template('game.html', word_display=word_display, incorrect_letters=guessed_letters, correct_letters=correct_letters, chances=chances, player_name=player_name, remaining_letters=remaining_letters)


@hangman_app.route('/reset/<player_name>', methods=['GET','POST'])
def reset_game(player_name):
    redis_store.delete(player_name)
    return redirect(url_for('play_game',player_name=player_name))


@hangman_app.route('/close/<player_name>', methods=['GET','POST'])
def close_game(player_name):
    redis_store.delete(player_name)
    return redirect(url_for('home_page_of_game'))

@hangman_app.route('/print_session')
def print_session():
    session_data = {}
    keys = redis_store.keys('*')
    for key in keys:
        session_data[key] = redis_store.get(key)
    return render_template('session.html', session_data=session_data)

if __name__ == '__main__':
    hangman_app.run()