import logging
from pathlib import Path
from io import BytesIO
import random
from db import GuessPictureDB
from blur_image import BlurImage
from shuffle_image import ShuffleImage
from mask_image import MaskImage

from PIL import Image
import PIL

import telebot

import bot_secrets

BLUR = 'blur'
MASK = 'mask'
SHUFFLE = 'shuffle'



logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)
db_guesser = GuessPictureDB()


@bot.message_handler(commands=['help', 'start'])
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
    user_id = message.from_user.id
    files = list(Path("pictures/").glob("*.jpg"))
    logger.info(f"test: {files}")
    random_image = db_guesser.get_random_image()
    # im: PIL.Image = Image.open(random_image['image_path'])
    # im2 = im.resize((200, 200))
    # im2 = im2.rotate(90)
    # bio = BytesIO()
    # bio.name = 'image.jpeg'
    blur_image = BlurImage(random_image['image_path'])
    shuffle_image = ShuffleImage(random_image['image_path'])
    mask_image = MaskImage(random_image['image_path'])

    db_guesser.add_chat(chat_id, user_id, random_image['image_path'], blur_image.hardness_index,BLUR)
    # photo_name = (im.filename.split('\\')[-1]).split('.')[0]
    # logger.info(f"name of image: {photo_name}")
    # im2.save(bio, 'JPEG')
    # blur = blur_image(random_image['image_path'])

    # bio.seek(0)
    print(blur_image.run_func())
    bot.send_photo(chat_id, blur_image.run_func())
    # bot.send_photo(chat_id, photo=bio)

    # bot.send_photo(chat_id, photo=open('kitty.jpg', 'rb'))


@bot.message_handler(commands=['guess'])
def check_guess(message: telebot.types.Message):
    chat_id = message.chat.id
    guess = " ".join(message.text.split(' ')[1:])
    guesser_id = message.from_user.id
    guesser_first_name = message.from_user.first_name
    correct_answers = db_guesser.get_name(chat_id)
    print(correct_answers)
    if correct_answers is None:
        logger.error("There is no pictures")
        return
    if guess in correct_answers:
        logger.info("Correct Answer")
        db_guesser.delete_picture(chat_id, guesser_id)
        bot.send_message(chat_id, f"Correct Guess, Do you want another picture {guesser_first_name}?")
        return

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
    bot.send_message(chat_id, f"NOT correct, try again {guesser_first_name}")
def object_start(type:str, image_path: str):
    if type == BLUR:
        return BlurImage(image_path)
    elif type == SHUFFLE:
        return ShuffleImage(image_path)
    elif type == MASK:
        return MaskImage(image_path)
@bot.message_handler(commands=['hint'])
def request_hint(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    game_session = db_guesser.chat.find_one({'chat_id': chat_id, 'user_id': user_id})['game_session']

    print(game_session)

    new_obj = object_start(game_session["game_type"], game_session["image_path"])
    new_obj.hardness_index = game_session["hardness"]
    if new_obj.make_easier():
        new_image = new_obj.run_func()
        db_guesser.changes_hardness(chat_id, user_id, new_obj.hardness_index)
        bot.send_photo(chat_id, new_image)
    else:
        logger.info("it cant be easier")


    # db_guesser.changes_hardness(chat_id, user_id, blur_image.hardness_index)




    # game_session = True
    # if not game_session:
    #     bot.send_message(chat_id, "there has to be an ongoing game to use this command")
    #     return
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
