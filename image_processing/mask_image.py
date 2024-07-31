import random
from shred_image import ShredImage
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

'''
hardness array VVV
index 0 = very-easy
index 1 = easy
index 2 = medium
index 3 = hard
hardness array AAA
'''


class MaskImage(ShredImage):
    def __init__(self, image_path):
        self.hardness = [15, 9, 4, 1]
        self.hardness_index = len(self.hardness) - 1
        self.image = self.importing_image(image_path)
        self.mask_box_size = 0.25
        self.boxes_coords = MaskImage.add_random_white_boxes(self)

    def run_func(self):
        window_width = int(self.image.width * self.mask_box_size)
        window_height = int(self.image.height * self.mask_box_size)
        hardness_value = self.hardness[self.hardness_index]
        mask = Image.new('RGBA', self.image.size, (0, 0, 0, 255))

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
        result = Image.alpha_composite(self.image.convert('RGBA'), mask)
        return result

    def add_random_white_boxes(self):
        num_boxes = self.hardness[0]
        # Create a copy of the image to avoid modifying the original
        width, height = self.image.size
        # Calculate box size (20% of the image)
        box_width = int(width * self.mask_box_size)
        box_height = int(height * self.mask_box_size)

        coordinates = []
        for _ in range(num_boxes):
            # Random position
            x = random.randint(0, width - box_width)
            y = random.randint(0, height - box_height)
            # Draw white box
            coordinates.append((x, y))
        return coordinates

    def make_easier(self):
        if self.hardness_index > 0:
            self.hardness_index -= 1
            return True
        return False


if __name__ == '__main__':
    test = MaskImage("../python_img.png")
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()
    test.make_easier()
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()
