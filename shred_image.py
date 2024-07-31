# import matplotlib.pyplot as plt
#
# import blur_image
# import mask_image
# import shuftle_image
# import numpy as np
from PIL import Image

pwd_path = "/Users/saldevfree/PycharmProjects/pythonProject/devboost1-telegram-bot-hackathon-cute-pandas/"


class ShredImage:
    def importing_image(self, image_path: str) -> Image:
        global pwd_path
        try:
            print(image_path)
            test = Image.open(image_path)
            print("after")
            return test
        except FileNotFoundError:
            edited_path = pwd_path + image_path
            try:
                print(image_path)
                test = Image.open(edited_path)
                print("after")
                return test
            except:
                pass

    '''TODO
        def importing_image(path:str):
            try:
            "importing ann opening instruction"
            except :
        '''

    def run_func(self) -> str:
        pass

    def make_easier(self):
        pass

# if __name__ == '__main__':
#     test_path = "python_img.png"
#     shuffle_image_obj = shuftle_image.ShuffleImage(test_path)
#     shuffle_image_test = shuffle_image_obj.run_func("medium")
#     plt.imshow(shuffle_image_test)
#     plt.show()
#     blur_image_obj = blur_image.BlurImage(test_path)
#     blur_image_test = blur_image_obj.run_func("medium")
#     plt.imshow(blur_image_test)
#     plt.show()
#     mask_image_obj = mask_image.MaskImage(test_path)
#     mask_image_test = mask_image_obj.run_func("medium")
#     plt.imshow(mask_image_test)
#     plt.show()
