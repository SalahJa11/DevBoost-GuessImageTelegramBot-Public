import logging
from pathlib import Path

from cutepandas.image_processing import image_factory
from db import GuessPictureDB
from autocorrect import Speller

import telebot
from telebot import types

import bot_secrets

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)
db_guesser = GuessPictureDB()
spell = Speller(lang='en')


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
    # user_id = message.from_user.id
    # files = list(Path("pictures/").glob("*.jpg"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Blur Image", callback_data= str(image_factory.Images.BLUR_IMAGE.value))
    button2 = types.InlineKeyboardButton("Mask Image", callback_data= str(image_factory.Images.MASK_IMAGE.value))
    button3 = types.InlineKeyboardButton("Shuffle Image", callback_data= str(image_factory.Images.SHUFFLE_IMAGE.value))
    keyboard.add(button1, button2, button3)

    bot.send_message(message.chat.id, "choose an option: ", reply_markup=keyboard)

    # logger.info(f"test: {files}")
    # random_image = db_guesser.get_random_image()
    # im: PIL.Image = Image.open(random_image['image_path'])
    # im2 = im.resize((200, 200))
    # im2 = im2.rotate(90)
    # bio = BytesIO()
    # bio.name = 'image.jpeg'
    # blur_image = BlurImage(random_image['image_path'])
    # shuffle_image = ShuffleImage(random_image['image_path'])
    # mask_image = MaskImage(random_image['image_path'])
    #
    # db_guesser.add_chat(chat_id, user_id, random_image['image_path'], blur_image.hardness_index, BLUR)
    # photo_name = (im.filename.split('\\')[-1]).split('.')[0]
    # logger.info(f"name of image: {photo_name}")
    # im2.save(bio, 'JPEG')
    # blur = blur_image(random_image['image_path'])

    # bio.seek(0)
    # print(blur_image.run_func())
    # bot.send_photo(chat_id, blur_image.run_func())
    # bot.send_photo(chat_id, photo=bio)

    # bot.send_photo(chat_id, photo=open('kitty.jpg', 'rb'))


@bot.callback_query_handler(func=lambda call: call.data == "hint")
def handle_hint_button(call):
    print(f"sadasdas {call}")
    # request_hint(call.message)
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    game_session = db_guesser.chat.find_one({'chat_id': chat_id, 'user_id': user_id})['game_session']

    print(game_session)

    new_obj = image_factory.image_factory(image_factory.Images(game_session["game_type"]), game_session["image_path"])
    new_obj.hardness_index = game_session["hardness"]
    if new_obj.make_easier():
        new_image = new_obj.run_func()
        db_guesser.changes_hardness(chat_id, user_id, game_session['image_path'], game_session['game_type'],
                                    new_obj.hardness_index)
        bot.send_photo(chat_id, new_image)
    else:
        bot.send_message(chat_id, "It can't be easier")
        logger.info("it cant be easier")
        return

    bot.edit_message_text("Guess the image:", chat_id=chat_id, message_id=call.message.id, reply_markup=None)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Hint!!", callback_data='hint')
    keyboard.add(button1)
    bot.send_message(chat_id, "Do you need a help?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in "123")
def handle_callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    random_image = db_guesser.get_random_image()

    choice = int(call.data)
    hidden_image = image_factory.image_factory(image_factory.Images(choice), random_image['image_path'])
    db_guesser.add_chat(chat_id, user_id, random_image['image_path'], hidden_image.hardness_index, choice)
    bot.send_photo(chat_id, hidden_image.run_func())
    bot.edit_message_text("Guess the image:", chat_id=chat_id, message_id=call.message.id, reply_markup=None)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Hint!!", callback_data='hint')
    keyboard.add(button1)
    bot.send_message(chat_id, "Do you need a help?", reply_markup=keyboard)


@bot.message_handler(commands=['guess'])
def check_guess(message: telebot.types.Message):
    if message.chat.type == 'private':
        guess = message.text
    else:
        guess = " ".join(message.text.split(' ')[1:])

    chat_id = message.chat.id
    guesser_id = message.from_user.id
    guesser_first_name = message.from_user.first_name
    correct_answers = db_guesser.get_name(chat_id)
    print(correct_answers)
    if correct_answers is None:
        logger.error("There is no pictures")
        return
    if guess in correct_answers or spell(guess) in correct_answers:
        logger.info("Correct Answer")
        db_guesser.delete_picture(chat_id, guesser_id)
        bot.send_message(chat_id, f"Correct Guess, Do you want another picture, write /play {guesser_first_name}?")
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
    # if message.text == 'hint':
    #     return
    bot.send_message(chat_id, f"NOT correct, try again {guesser_first_name}, if you need a hint click /hint")

@bot.message_handler(commands=['hint'])
def request_hint(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    game_session = db_guesser.chat.find_one({'chat_id': chat_id, 'user_id': user_id})['game_session']

    print(game_session)

    new_obj = image_factory.image_factory(image_factory.Images(game_session["game_type"]), game_session["image_path"])
    new_obj.hardness_index = game_session["hardness"]
    if new_obj.make_easier():
        new_image = new_obj.run_func()
        db_guesser.changes_hardness(chat_id, user_id, game_session['image_path'], game_session['game_type'],
                                    new_obj.hardness_index)
        bot.send_photo(chat_id, new_image)
    else:
        bot.send_message(chat_id, "It can't be easier")
        logger.info("it cant be easier")


@bot.message_handler(func=lambda message: True)
def nothing(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    logger.info(f"= Got on chat #{chat_id}/{username!r}: {text!r}")
    if message.chat.type == 'private':
        if message.text == 'play':
            start_game(message)
        elif message.text == 'hint':
            request_hint(message)
        else:
            check_guess(message)

logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
