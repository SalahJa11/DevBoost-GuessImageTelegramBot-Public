from shred_image import ShredImage
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt


class BlurImage(ShredImage):
    def __init__(self, img):
        # self.hardness = [7, 5, 3, 2]
        self.hardness = {"hard": 70, "medium": 45, "easy": 25, "very-easy": 14}
        self.image = img

    def run_func(self, hardness="hard"):
        img = Image.open("python_img.png")
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=self.hardness[hardness]))
        # plt.imshow(blurred_img)
        # plt.show()
        return blurred_img

    # def simplify_func(self,) -> dict:
if __name__ == '__main__':
    BlurImage(None).run_func(hardness="hard")