import logging
import random

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
    user_id = message.from_user.id
    username = message.from_user.username
    update_user(chat_id, user_id)
    logger.info(f"> Start chat #{chat_id}. username: {username}")
    response = """
This is a guess the image game.
The bot will send an image and the users will have to guess what's in the image.
Commands:
/help - Display instructions. 
/play - Starts the game showing an image to guess.
/score , /end - Displays the player's score. 
Commands during game:
/guess <your_answer> - Submit a guess.
/hint - Request a hint.
In private chat:
You can write play without the /. 
You can use /guess <word> without /guess only <word> 

"""
    bot.send_message(chat_id, response)


@bot.message_handler(commands=['play'])
def start_game(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    update_user(chat_id, user_id)

    if message.chat.type == 'private':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton("Blur Image", callback_data= str(image_factory.Images.BLUR_IMAGE.value))
        button2 = types.InlineKeyboardButton("Mask Image", callback_data= str(image_factory.Images.MASK_IMAGE.value))
        button3 = types.InlineKeyboardButton("Shuffle Image", callback_data= str(image_factory.Images.SHUFFLE_IMAGE.value))
        keyboard.add(button1, button2, button3)

        bot.send_message(message.chat.id, "choose an option: ", reply_markup=keyboard)

    else:
        current_chat = db_guesser.find_one_chat(chat_id)
        visited = current_chat["visited"] if "visited" in current_chat else []
        print(f"visited images: {visited}")
        random_image = db_guesser.get_random_image(visited)
        if not random_image:
            print("got none image")
            db_guesser.empty_visited(chat_id, user_id)
            visited = []
            random_image = db_guesser.get_random_image(visited)
        print(f"random image i got is: {random_image}")

        visited.append(random_image['image_path'])
        db_guesser.add_visited_to_chat(chat_id, visited)

        choice = random.randint(0,2)
        hidden_image = image_factory.image_factory(image_factory.Images(choice), random_image['image_path'])
        db_guesser.add_session(chat_id, random_image["image_path"], choice, hidden_image.hardness_index)
        bot.send_photo(chat_id, hidden_image.run_func(), caption="Guess the image!")


@bot.callback_query_handler(func=lambda call: call.data == "hint")
def handle_hint_button(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    update_user(chat_id, user_id)
    if process_hint_request(chat_id, user_id):
        bot.edit_message_text("Guess the image:", chat_id=chat_id, message_id=call.message.id, reply_markup=None)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton("Hint!!", callback_data='hint')
        keyboard.add(button1)
        bot.send_message(chat_id, "Do you need a help?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in "012")
def handle_callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    current_chat = db_guesser.find_one_chat(chat_id)
    visited = current_chat["visited"] if "visited" in current_chat else []
    print(f"visited images: {visited}")
    random_image = db_guesser.get_random_image(visited)
    if not random_image:
        print("got none image")
        db_guesser.empty_visited(chat_id, user_id)
        visited = []
        random_image = db_guesser.get_random_image(visited)
    # if random_image is None:
    #     db_guesser.add_visited_to_chat()
    print(f"random image i got is: {random_image}")

    choice = int(call.data)
    hidden_image = image_factory.image_factory(image_factory.Images(choice), random_image['image_path'])
    # db_guesser.add_chat(chat_id, user_id, random_image['image_path'], hidden_image.hardness_index, choice)
    db_guesser.add_session(chat_id, random_image["image_path"], choice, hidden_image.hardness_index)
    bot.send_photo(chat_id, hidden_image.run_func())
    bot.edit_message_text("Guess the image:", chat_id=chat_id, message_id=call.message.id, reply_markup=None)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Hint!!", callback_data='hint')
    keyboard.add(button1)
    bot.send_message(chat_id, "Do you need a help?", reply_markup=keyboard)

    visited.append(random_image['image_path'])
    db_guesser.add_visited_to_chat(chat_id, visited)


@bot.message_handler(commands=['guess'])
def check_guess(message: telebot.types.Message):
    chat_id = message.chat.id
    guesser_id = message.from_user.id
    guesser_first_name = message.from_user.first_name

    update_user(chat_id, guesser_id)

    if not check_session(db_guesser.find_session(chat_id)):
        return

    if message.chat.type == 'private':
        guess = message.text
    else:
        guess = " ".join(message.text.split(' ')[1:])
    guess = guess.lower()

    correct_answers = db_guesser.get_name(chat_id)
    print(correct_answers)
    if correct_answers is None:
        logger.error("There is no pictures")
        return
    if guess in correct_answers or spell(guess) in correct_answers:
        logger.info("Correct Answer")
        db_guesser.update_score(chat_id, guesser_id)
        db_guesser.remove_session(chat_id)
        bot.send_message(chat_id, f"Correct Guess, Do you want another picture, write /play {guesser_first_name}?")
    else:
        bot.send_message(chat_id, f"NOT correct, try again {guesser_first_name}, if you need a hint click /hint")

    bot.send_message(chat_id, f"End Game /end")
    logger.info(f"the guess is: {guess}, it was made by: {guesser_first_name}")
    logger.info(message.from_user)
    # if message.text == 'hint':
    #     return

@bot.message_handler(commands=['end', 'score'])
def end_game(message: telebot.types.Message):
    ob = db_guesser.chat.find_one({"chat_id": message.chat.id, "user_id": message.from_user.id})
    if ob is None:
        bot.send_message(message.chat.id, f"you are not part of the game")
        return
    print(f"chat id {message.chat.id}     user id {message.from_user.id}")
    print(ob)
    score = ob["score"] if "score" in ob else 0
    bot.send_message(message.chat.id, f"Your score is {score}")
@bot.message_handler(commands=['hint'])
def request_hint(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    process_hint_request(chat_id, user_id)

@bot.message_handler(func=lambda message: True)
def nothing(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    logger.info(f"= Got on chat #{chat_id}/{username!r}: {text!r}")
    if message.chat.type == 'private':
        lower_text = message.text.lower()
        if lower_text == 'play':
            start_game(message)
        elif lower_text == 'hint':
            request_hint(message)
        else:
            check_guess(message)
def check_session(session_doc):
    if session_doc is None:
        logger.info("there is no ongoing session for this chat")
        return False
    return True

def process_hint_request(chat_id: int, user_id: int):

    chat_session = db_guesser.find_session(chat_id)
    logger.info(chat_session)
    update_user(chat_id, user_id)
    if not check_session(chat_session):
        return False

    new_obj = image_factory.image_factory(image_factory.Images(chat_session["game_type"]), chat_session["image_path"])
    new_obj.hardness_index = chat_session["hardness"]
    logger.info(f"object is: {new_obj}")
    logger.info(f"hardness index is: {new_obj.hardness_index}")
    if new_obj.make_easier():
        new_image = new_obj.run_func()
        db_guesser.update_session_hardness(chat_id, new_obj.hardness_index)
        # db_guesser.changes_hardness(chat_id, user_id, game_session['image_path'], game_session['game_type'],
        #                             new_obj.hardness_index)
        bot.send_photo(chat_id, new_image)
    else:
        bot.send_message(chat_id, "It can't be easier")
        logger.info("it cant be easier")
        return False

    return True

def update_user(chat_id, user_id):
    db_guesser.add_chat(chat_id, user_id)

logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
