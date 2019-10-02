import math
import numpy as np

def nearestNeighbor(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = w1 / float(w2)
    y_ratio = h1 / float(h2)
    new_matrix = np.zeros((h2, w2))
    for i in range(h2):
        for j in range(w2):
            px = math.floor(j * x_ratio)
            py = math.floor(i * y_ratio)
            new_matrix[i][j] = img_matrix[py][px]
    return new_matrix

def linearX(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = float(w1 - 1) / w2
    y_ratio = float(h1) / h2
    new_matrix = np.zeros((h2, w2))
    for i in range(h2):
        for j in range(w2):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            A = img_matrix[y][x]
            B = img_matrix[y][x+1]
            x_diff = (x_ratio * j) - x
            new_pixel_value = int(A * (1 - x_diff) + B * x_diff)
            new_matrix[i][j] = new_pixel_value
    return new_matrix

def linearY(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = float(w1) / w2
    y_ratio = float(h1 - 1) / h2
    new_matrix = np.zeros((h2, w2))
    for i in range(h2):
        for j in range(w2):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            A = img_matrix[y][x]
            C = img_matrix[y+1][x]
            y_diff = (y_ratio * i) - y
            new_pixel_value = int(A * (1 - y_diff) + C * y_diff)
            new_matrix[i][j] = new_pixel_value
    return new_matrix

def linearY(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = float(w1) / w2
    y_ratio = float(h1 - 1) / h2
    new_matrix = np.zeros((h2, w2))
    for i in range(h2):
        for j in range(w2):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            A = img_matrix[y][x]
            C = img_matrix[y+1][x]
            y_diff = (y_ratio * i) - y
            new_pixel_value = int(A * (1 - y_diff) + C * y_diff)
            new_matrix[i][j] = new_pixel_value
    return new_matrix

def bilinear(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = float(w1 - 1) / w2
    y_ratio = float(h1 - 1) / h2
    new_matrix = np.zeros((h2, w2))
    for i in range(h2):
        for j in range(w2):
            x = int(x_ratio * j)
            y = int(y_ratio * i)
            A = img_matrix[y][x]
            B = img_matrix[y][x+1]
            C = img_matrix[y+1][x]
            D = img_matrix[y+1][x+1]
            x_diff = (x_ratio * j) - x
            y_diff = (y_ratio * i) - y
            new_pixel_val = int(A * (1 - x_diff) * (1 - y_diff) 
                      + B * (x_diff) * (1 - y_diff)
                      + C * (y_diff) * (1 - x_diff)
                      + D * (x_diff * y_diff))
            new_matrix[i][j] = new_pixel_val
    return new_matrix

def convertGrayLevel(img_array, ori_gray_level, new_gray_level):
    ori_pixel_range = 2 ** ori_gray_level
    new_pixel_range = 2 ** new_gray_level
    ratio = float(new_pixel_range) / float(ori_pixel_range)
    new_img_array = np.copy(img_array)
    for row in range(len(img_array)):
        for col in range(len(img_array[row])):
            new_img_array[row][col] = int(img_array[row][col] * ratio) * (256 / (2 ** new_gray_level))
    return new_img_array

def global_histogram_equalization(img_matrix):
    intensity_count = [0.0] * 256
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[row])):
            intensity_count[img_matrix[row][col]] += 1
    intensity_probability = [0.0] * 256
    total_pixels = len(img_matrix) * len(img_matrix[0])
    for index in range(256):
        intensity_probability[index] = intensity_count[index] / total_pixels
    for index in range(1, 256):
        intensity_probability[index] += intensity_probability[index - 1]
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[row])):
            img_matrix[row][col] = int(intensity_probability[img_matrix[row][col]] * 255.0)
    return img_matrix