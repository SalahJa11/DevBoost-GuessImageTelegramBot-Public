# import matplotlib.pyplot as plt
#
# import blur_image
# import mask_image
# import shuftle_image
# import numpy as np
import os
from PIL import Image
import os
import sys
# Get the parent directory
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# sys.path.insert(0, parent_dir)

class ShredImage:
    def importing_image(self, image_path: str) -> Image:
        try:
            test = Image.open(image_path)
            return test
        except FileNotFoundError:
            edited_path = os.path.join(PICTURES_PATH, image_path)
            try:
                test = Image.open(edited_path)
                return test
            except:
                print("importing failure")
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
