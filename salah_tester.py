from matplotlib import pyplot as plt

import blur_image
import mask_image
import shuffle_image

if __name__ == '__main__':
    test_path = "python_img.png"
    shuffle_image_obj = shuffle_image.ShuffleImage(test_path)
    shuffle_image_test = shuffle_image_obj.run_func()
    plt.imshow(shuffle_image_test)
    plt.show()
    blur_image_obj = blur_image.BlurImage(test_path)
    blur_image_test = blur_image_obj.run_func()
    plt.imshow(blur_image_test)
    plt.show()
    mask_image_obj = mask_image.MaskImage(test_path)
    mask_image_test = mask_image_obj.run_func()
    plt.imshow(mask_image_test)
    plt.show()
