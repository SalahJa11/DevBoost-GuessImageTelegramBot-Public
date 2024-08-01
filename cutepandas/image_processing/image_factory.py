from enum import Enum

from cutepandas.image_processing.blur_image import BlurImage
from cutepandas.image_processing.mask_image import MaskImage
from cutepandas.image_processing.shuffle_image import ShuffleImage


class Images(Enum):
    SHUFFLE_IMAGE = 0
    MASK_IMAGE = 1
    BLUR_IMAGE = 2


def image_factory(type: Images, image_path: str):
    if type == Images.BLUR_IMAGE:
        return BlurImage(image_path)
    if type == Images.SHUFFLE_IMAGE:
        return ShuffleImage(image_path)
    if type == Images.MASK_IMAGE:
        return MaskImage(image_path)


if __name__ == "__main__":
    print("testing some things here")
    print(image_factory(Images(2), "../pictures/cat.jpg"))
