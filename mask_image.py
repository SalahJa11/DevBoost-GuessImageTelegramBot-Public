import random
from shred_image import ShredImage
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


class MaskImage(ShredImage):
    def __init__(self, img):
        # self.hardness = [7, 5, 3, 2]
        self.hardness = {"hard": 1, "medium": 4, "easy": 9, "very-easy": 15}
        self.image = img
        self.boxes_coords = MaskImage.add_random_white_boxes(img)

    def run_func(self, hardness="hard"):
        img = Image.open("python_img.png")
        window_size = 0.2
        window_width = int(img.width * window_size)
        window_height = int(img.height * window_size)

        hardness_value = self.hardness[hardness]
        mask = Image.new('RGBA', img.size, (0, 0, 0, 255))

        for i in range(hardness_value):
            x1 = self.boxes_coords[i][0]
            y1 = self.boxes_coords[i][1]
            x2 = x1 + window_width
            y2 = y1 + window_height

            # Create a draw object
            draw = ImageDraw.Draw(mask)


            # Draw a semi-transparent rectangle for the window
            draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 0))

            # Combine the original image with the mask

        img = Image.alpha_composite(img.convert('RGBA'), mask)
        # result = Image.alpha_composite(img.convert('RGBA'), mask)

        # return blurred_img
        plt.imshow(img)
        plt.show()



    def add_random_white_boxes(self, num_boxes=15):

        image = Image.open("python_img.png")
        box_size = 0.2
        # Create a copy of the image to avoid modifying the original
        width, height = image.size
        # Calculate box size (20% of the image)
        box_width = int(width * box_size)
        box_height = int(height * box_size)

        coordinates = []
        for _ in range(num_boxes):
            # Random position
            x = random.randint(0, width - box_width)
            y = random.randint(0, height - box_height)
            # Draw white box
            coordinates.append((x, y))
        return coordinates

    # def simplify_func(self,) -> dict:
if __name__ == '__main__':
    MaskImage("python_img.png").run_func(hardness="easy")
