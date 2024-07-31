# 🚀 Guess image game bot

## The Team
- 💡 Ofir
- 💡 Adam
- 💡 Salah
- 💡 Kateryna

## About guess image game bot

This bot allows you to play game 🤖.
The purpose of the game is to guess object on the displayed picture.
The difficulty is that the picture is shown either partially or in low quality, so that guessing is more interesting.
If the player guesses correctly, he wins and earns a plus to his player rating.
It is possible to choose the difficulty of the game.

🔗 Here is the link to add bot: @devBoost_Kate_bot

You can play alone or to add this bot to your group and play with friends. Just need to make it admin. 

## Instructions for Developers 
### Prerequisites
- Python 3.11
- Poetry
- MongoDB

### Setup
- git clone this repository 
- cd into the project directory
- Install dependencies:
    
      poetry install


- Get an API Token for a bot via the [BotFather](https://telegram.me/BotFather)
- Create a `bot_settings.py` file with your bot token:

      BOT_TOKEN = 'xxxxxxx'

### Running tests        

      poetry run pytest


### Running the bot        
- Run the bot:

      poetry run python bot.py
