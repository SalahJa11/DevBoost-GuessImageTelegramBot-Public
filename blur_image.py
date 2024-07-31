from shred_image import ShredImage
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

'''
hardness array VVV
index 0 = very-easy
index 1 = easy
index 2 = medium
index 3 = hard
hardness array AAA
'''

class BlurImage(ShredImage):
    def __init__(self, image_path):
        # self.hardness = [7, 5, 3, 2]
        self.hardness = [14, 25, 45, 70]
        self.hardness_index = len(self.hardness) - 1
        self.image = self.importing_image(image_path)

    def run_func(self):
        blurred_img = self.image.filter(ImageFilter.GaussianBlur(radius=self.hardness[self.hardness_index]))
        return blurred_img
    def make_easier(self):
        if self.hardness_index > 0:
            self.hardness_index -= 1
            return True
        return False
    # def simplify_func(self,) -> dict:
if __name__ == '__main__':
    test = BlurImage("python_img.png")
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()
    test.make_easier()
    test_image = test.run_func()
    plt.imshow(test_image)
    plt.show()