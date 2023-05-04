# Hangman_game

## Start Instructions
1. Clone the repository and navigate to the hangman_game folder in your IDE or terminal.

2. In the terminal run following command to install all the dependencies.
   pip install -r requirements.txt

3. Run the game using command
   python hangman.py 

4. Visit the link http://127.0.0.1:5000 or the link shown in your terminal if different

### Notes:
Please do check verify if redis is installed on your device otherwise follow the link given below if you are using windows <a href="https://youtu.be/8OcOv7wh82Y" target="_blank">Redis Installation</a>

Also look out for the redis port number and database number in hangman.py and modify following line
hangman_app.config['SESSION_REDIS_URL'] = 'redis://localhost:6379/0'

Here 6379 is the port where redis server is running and 0 indicates the first database. 

## Flask Redis Session
Main challenge:
To store the games sessions and restore when player gets back

Redis Sessions:
As redis allows to store data in key-value pair, I stored player_name as key and current game state of that player in value for session.
Game state involes data like...
a) word_display : It shows underscore for the letters remaining to be guessed in word itself and shows the letter that are correctly guessed
b) word : It is the word that player needs to guess
c) guessed_letters : It contains list of letters that have been guessed by users but are not in the word ot guess
d) correct_letters : It contains list of letters that have been guessed by users correctly
e) chances : It the remainig number of guess player can take (initaily its set to 6).

Functions implemented:
There are in total 5 functions with different routes associated with them.

1. home_page_of_game ('/') : When ever player starts the game, they see home page that welcomes the player and ask for their name.

2. play_game ('/inGame/<player_name>') : Taking player's name, game is started at this function. It checks for player_name in all active sessions on redis. If found loads the game from that state otherwise initalizes game as for new player and renders the game.

3. reset_game ('reset/<player_name>') : When player wants to reset the game, they can reset it by clicking reset button. It removes the current session of that player from redis and redirects to play_game where this player will be considered as new player.

4. close_game ('close/<player_name') : When player press close button, it will delete that player's session from redis and redirects to home page.

5. print_session ('/print_session') : It displays all the active sessions from redis database.

### There is lot to work on. But I hope you find the game interesting.


