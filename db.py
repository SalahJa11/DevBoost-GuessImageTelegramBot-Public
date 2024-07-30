import os
import random

from pymongo import MongoClient


class GuessPictureDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database("Guess_picture_bot")
        self.chat = self.db.get_collection("chat")
        self.pictures = self.db.get_collection("Pictures")

        # self.lists.create_index("chat_id", unique=True)

    def add_chat(self, chat_id, right_name):
        self.chat.update_one({'chat_id': chat_id}, {
            '$set': {'right_name': right_name}
        }, upsert=True)


    def get_name(self, chat_id):
        ret = self.chat.find_one({'chat_id': chat_id})
        return ret["right_name"] if ret is not None else None




    def get_random_picture_path(self, folder_dir: str) -> str:
        picture_files = [
            f for f in os.listdir(folder_dir) if f.endswith(("jpg", "jpeg", "png"))
        ]
        return (
            os.path.join(folder_dir, random.choice(picture_files))
            if picture_files
            else None
        )


# PICTURES_DIR = "/Users/kateryna/PycharmProjects/devboost1-telegram-bot-hackathon-cute-pandas/pictures"


if __name__ == '__main__':
    folder_dir = "pictures"
    guesser = GuessPictureDB()
    for img in os.listdir(folder_dir):
        print(img)



    guesser.add_chat("", 'cat')
