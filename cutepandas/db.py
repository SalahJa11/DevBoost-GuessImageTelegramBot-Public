import os
import random
import json
from pymongo import MongoClient


class GuessPictureDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database("Guess_picture_bot")
        self.chat = self.db.get_collection("chat")
        self.pictures = self.db.get_collection("Pictures")
        self.sessions = self.db.get_collection("Sessions")
        self.chat.create_index('chat_id')
        self.pictures.create_index('image_path')
        self.sessions.create_index('chat_id')

        # self.lists.create_index("chat_id", unique=True)

    def add_chat(self, chat_id, user_id, score = 0):
        self.chat.update_one({'chat_id': chat_id, 'user_id': user_id}, {
            '$set': {}
        }, upsert=True)

    def add_empty_chat(self, chat_id, user_id):
        self.chat.update_one({'chat_id' : chat_id , 'user_id' : user_id}, {'$set' : {}}, upsert=True)

    def add_visited_to_chat(self, chat_id, visited):
        self.chat.update_one({'chat_id' : chat_id}, {'$set': {'visited' : visited}}
                             , upsert=True)

    def find_one_chat(self, chat_id):
        return self.chat.find_one({'chat_id' : chat_id})


# Todo : It's not update the increment because i delete and create another one, also I update
    #  on it without score in add_chat maybe i should create another table with score or just delete field
    #  that related to photo
    def update_score(self, chat_id, user_id):
        self.chat.update_one({'chat_id': chat_id, 'user_id' : user_id},
                             {'$inc': {'score': 10}
        }, upsert=True)

    def get_name(self, chat_id):
        # ret = self.chat.find_one({'chat_id': chat_id})['game_session']['image_path']
        ret = self.find_session(chat_id)["image_path"]
        return self.pictures.find_one({'image_path': ret})['synonyms'] if ret is not None else None

    def add_pictures(self, data_file):
        for k, synonyms in data_file.items():
            print(k)
            self.pictures.update_one({"image_path": k}, {
                '$set': {"synonyms": synonyms}
            }, upsert=True)
            # print(k ,synonyms)

        # for img in folder:
        #     self.pictures.insert_many()

    # maybe I want the bot to add score by number! without guessing
    def set_score(self):
        ...

    def get_random_image(self, visited=[]):
        for item in self.pictures.aggregate([{ '$match': { 'image_path': { '$nin' : visited}}},{'$sample': {'size': 1}}]):
            return item
        return None

    def changes_hardness(self, chat_id, user_id, image_path, game_type,hardness):
        self.chat.update_one({'chat_id': chat_id, 'user_id': user_id},
                             {'$set': {'game_session': {'image_path': image_path, 'game_type': game_type,
                                                        'hardness': hardness}}})

    def add_session(self, chat_id: int, image_path: str, game_type, hardness):
        self.sessions.update_one({'chat_id' : chat_id}, {'$set' : {'chat_id' : chat_id, 'image_path' : image_path, 'game_type' : game_type, 'hardness' : hardness}}, upsert=True)

    def update_session_hardness(self, chat_id: int, hardness):
        self.sessions.update_one({'chat_id' : chat_id}, {'$set' : {'hardness' : hardness}})

    def find_session(self, chat_id: int):
        return self.sessions.find_one({'chat_id' : chat_id})

    def remove_session(self, chat_id: int):
        self.sessions.delete_one({'chat_id' : chat_id})


    # def get_random_picture_path(self, folder_dir: str) -> str:
    #     picture_files = [
    #         f for f in os.listdir(folder_dir) if f.endswith(("jpg", "jpeg", "png"))
    #     ]
    #     return (
    #         os.path.join(folder_dir, random.choice(picture_files))
    #         if picture_files
    #         else None
    #     )


# PICTURES_DIR = "/Users/kateryna/PycharmProjects/devboost1-telegram-bot-hackathon-cute-pandas/pictures"


if __name__ == '__main__':
    folder_dir = "pictures"
    guesser = GuessPictureDB()
    # guesser.add_pictures(os.listdir(folder_dir))
    with open("Synonyms_words.json", 'r') as f:
        data = json.load(f)
    guesser.add_pictures(data)

    print(data)
    for img in os.listdir(folder_dir):
        print(img)

# options for answers   V
# score to each one (group chat >> chat_id &  message.from_user.id )  V
# do twice /play will update the db to last picture bot did give   V
