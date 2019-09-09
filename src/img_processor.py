import numpy as np

def convert_gray_level(img_array, ori_gray_level, new_gray_level):
    ori_pixel_range = 2 ** ori_gray_level
    new_pixel_range = 2 ** new_gray_level
    ratio = float(new_pixel_range) / float(ori_pixel_range)
    new_img_array = np.copy(img_array)
    for row in range(len(img_array)):
        for col in range(len(img_array[row])):
            new_img_array[row][col] = int(img_array[row][col] * ratio) * (256 / (2 ** new_gray_level))
    return new_img_array