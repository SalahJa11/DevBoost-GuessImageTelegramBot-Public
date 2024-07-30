import logging
from pathlib import Path
from io import BytesIO
import random
from db import GuessPictureDB


from PIL import Image
import PIL

import telebot

import bot_secrets

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)
guesser = GuessPictureDB()


@bot.message_handler(commands=['help'])
def display_help(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    logger.info(f"> Start chat #{chat_id}. username: {username}")
    response = """
This is a guess the image game.
The bot will send an image and the users will have to guess what's in the image.
Commands:
for instructions type /help
To start the game type /play
Commands during game:
To submit a guess type /guess <your_answer>
To request a hint type /hint 
"""
    bot.send_message(chat_id, response)


@bot.message_handler(commands=['play'])
def start_game(message: telebot.types.Message):
    chat_id = message.chat.id

    files = list(Path("pictures/").glob("*.jpg"))
    logger.info(f"test: {files}")

    im: PIL.Image = Image.open(random.choice(files))
    im2 = im.resize((200, 200))
    im2 = im2.rotate(90)
    bio = BytesIO()
    bio.name = 'image.jpeg'
    photo_name = (im.filename.split('\\')[-1]).split('.')[0]
    guesser.add_chat(chat_id, photo_name)
    logger.info(f"name of image: {photo_name}")
    im2.save(bio, 'JPEG')
    bio.seek(0)
    bot.send_photo(chat_id, photo=bio)

    # bot.send_photo(chat_id, photo=open('kitty.jpg', 'rb'))



@bot.message_handler(commands=['guess'])
def check_guess(message: telebot.types.Message):
    chat_id = message.chat.id
    guess = " ".join(message.text.split(' ')[1:])
    guesser_id = message.from_user.id
    guesser_first_name = message.from_user.first_name
    correct_name = guesser.get_name(chat_id)
    if correct_name is None:
        logger.error("There is no pictures")
        return
    if correct_name == guess:
        logger.info("correct")
    # player = get_player(guesser_id)
    # image = session(chat_id).get_image()
    # if image.check_guess(guess):
    #     logger.info(f"the guess is correct")
    #     # update score for this player, advertise correct and end the game session
    # else:
    #     logger.info(f"the guess is incorrect")
    #     # no updates, once time is up then goes to next hint

    logger.info(f"the guess is: {guess}, it was made by: {guesser_first_name}")
    logger.info(message.from_user)
    bot.send_message(chat_id, f"i dont know whether its correct or not, thank you {guesser_first_name}")

@bot.message_handler(commands=['hint'])
def request_hint(message: telebot.types.Message):
    chat_id = message.chat.id

    game_session = True
    if not game_session:
        bot.send_message(chat_id, "there has to be an ongoing game to use this command")
        return
    # bot.send_photo(chat_id, photo=open('kitty.jpg', 'rb'), caption="there is your hint")


@bot.message_handler(func=lambda message: True)
def nothing(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    logger.info(f"= Got on chat #{chat_id}/{username!r}: {text!r}")


logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
