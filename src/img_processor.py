import math
import numpy as np

def nearestNeighbor(img_array, w2, h2):
    one_dimension_img_array = img_array.flatten()
    w1 = len(img_array[0])
    h1 = len(img_array)
    x_ratio = w1 / float(w2)
    y_ratio = h1 / float(h2)
    px, py = 0, 0
    new_array = np.arange(w2 * h2)
    for i in range(h2):
        for j in range(w2):
            px = math.floor(j * x_ratio)
            py = math.floor(i * y_ratio)
            new_array[(i * w2) + j] = one_dimension_img_array[int((py * w1) + px)]
    return new_array.reshape(w2, h2)

def bilinear(img_array, w2, h2):
    one_dimension_img_array = img_array.flatten()
    w1 = len(img_array[0])
    h1 = len(img_array)
    x_ratio = float(w1 - 1) / w2
    y_ratio = float(h1 - 1) / h2
    offset = 0
    new_array = np.arange(w2 * h2)
    for i in range(h2):
        for j in range(w2):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            x_diff = (x_ratio * j) - x
            y_diff = (y_ratio * i) - y
            index = y * w1 + x
            A = one_dimension_img_array[index] & 0xff
            B = one_dimension_img_array[index + 1] & 0xff
            C = one_dimension_img_array[index + w1] & 0xff
            D = one_dimension_img_array[index + w1 + 1] & 0xff
            gray = int(A * (1 - x_diff) * (1 - y_diff) 
                      + B * (x_diff) * (1 - y_diff)
                      + C * (y_diff) * (1 - x_diff)
                      + D * (x_diff * y_diff))
            new_array[offset] = gray
            offset += 1
    return new_array.reshape(w2, h2)

def convertGrayLevel(img_array, ori_gray_level, new_gray_level):
    ori_pixel_range = 2 ** ori_gray_level
    new_pixel_range = 2 ** new_gray_level
    ratio = float(new_pixel_range) / float(ori_pixel_range)
    new_img_array = np.copy(img_array)
    for row in range(len(img_array)):
        for col in range(len(img_array[row])):
            new_img_array[row][col] = int(img_array[row][col] * ratio) * (256 / (2 ** new_gray_level))
    return new_img_array