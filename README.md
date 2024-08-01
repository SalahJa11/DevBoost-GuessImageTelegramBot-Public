# 🚀 Guess image game bot

## The Team
- 💡 Ofir
- 💡 Adam
- 💡 Salah
- 💡 Kateryna

## About guess image game bot

This bot allows you to play game 🤖.
The purpose of the game is to guess what is displayed on the picture picture.
The difficulty is that the picture is shown either partially or blurred or shuffled, so that guessing is more interesting.
If the player guesses correctly, he wins and earns a plus to his player rating.
It is possible to ask for a hint :)

🔗 Here is the link to add bot: @devBoost_Kate_bot

You can play alone but it's more fun to play with friends in group. Just need to make it admin. 

Here is some screenshots:
![telegram-cloud-photo-size-2-5285387918849989212-m](https://github.com/user-attachments/assets/c813094d-6e8a-42bf-9955-434be53f5c51)

## Instructions for Developers 
### Prerequisites
- Python 3.12
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
