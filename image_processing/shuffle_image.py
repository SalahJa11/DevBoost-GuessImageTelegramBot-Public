import math
import random
from PIL import Image
import matplotlib.pyplot as plt

from image_processing.shred_image import ShredImage

'''
hardness array VVV
index 0 = very-easy
index 1 = easy
index 2 = medium
index 3 = hard
hardness array AAA
'''


class ShuffleImage(ShredImage):
    def __init__(self, image_path):
        # self.hardness = [7, 5, 3, 2]
        self.hardness = [2, 3, 5, 7]
        self.hardness_index = len(self.hardness) - 1
        self.image = self.importing_image(image_path)

    def run_func(self):

        dim_1_pieces = self.hardness[self.hardness_index]

        # Calculate piece size
        piece_width = math.ceil(self.image.size[0] / dim_1_pieces)
        piece_height = math.ceil(self.image.size[1] / dim_1_pieces)

        # Create pieces
        pieces = []
        for y in range(0, self.image.size[1], piece_height):
            for x in range(0, self.image.size[0], piece_width):
                right = min(x + piece_width, self.image.size[0])
                bottom = min(y + piece_height, self.image.size[1])
                pieces.append((x, y, right, bottom))

        random.shuffle(pieces)
        new_image = Image.new('RGBA', self.image.size)

        for i, (x, y, right, bottom) in enumerate(pieces):
            # Crop the piece
            region = self.image.crop((x, y, right, bottom))

            # Calculate new position
            new_x = (i % dim_1_pieces) * piece_width
            new_y = (i // dim_1_pieces) * piece_height

            # Paste the piece
            new_image.paste(region, (new_x, new_y))

        return new_image

    # def simplify_func(self,) -> dict:
    def make_easier(self):
        if self.hardness_index > 0:
            self.hardness_index -= 1
            return True
        return False

if __name__ == '__main__':
    test = ShuffleImage("../python_img.png")
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()
    test.make_easier()
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()
