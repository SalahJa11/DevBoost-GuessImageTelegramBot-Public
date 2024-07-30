import math
import random
from PIL import Image
import matplotlib.pyplot as plt

from shred_image import ShredImage


class ShuffleImage(ShredImage):
    def __init__(self, img):
        # self.hardness = [7, 5, 3, 2]
        self.hardness = {"hard": 7, "medium": 5, "easy": 3, "very-easy": 2}
        self.image = img

    def run_func(self, hardness="hard"):
        im = Image.open("python_img.png")
        dim_1_pieces = self.hardness[hardness]

        # Calculate piece size
        piece_width = math.ceil(im.size[0] / dim_1_pieces)
        piece_height = math.ceil(im.size[1] / dim_1_pieces)

        # Create pieces
        pieces = []
        for y in range(0, im.size[1], piece_height):
            for x in range(0, im.size[0], piece_width):
                right = min(x + piece_width, im.size[0])
                bottom = min(y + piece_height, im.size[1])
                pieces.append((x, y, right, bottom))

        random.shuffle(pieces)
        new_image = Image.new('RGBA', im.size)

        for i, (x, y, right, bottom) in enumerate(pieces):
            # Crop the piece
            region = im.crop((x, y, right, bottom))

            # Calculate new position
            new_x = (i % dim_1_pieces) * piece_width
            new_y = (i // dim_1_pieces) * piece_height

            # Paste the piece
            new_image.paste(region, (new_x, new_y))

        # plt.imshow(new_image)
        # plt.show()
        return new_image

    # def simplify_func(self,) -> dict:

if __name__ == '__main__':
    a = ShuffleImage(None).run_func(hardness="very-easy")
