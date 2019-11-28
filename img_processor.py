import sys
import math
import numpy as np
import time
from functools import cmp_to_key

'''
Resizing algorithms
'''
def nearestNeighbor(img_matrix, w2, h2):
    w1 = len(img_matrix[0])
    h1 = len(img_matrix)
    x_ratio = w1 / float(w2)
    y_ratio = h1 / float(h2)
    new_matrix = np.zeros((h2, w2), dtype=np.int32)
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
    new_matrix = np.zeros((h2, w2), dtype=np.int32)
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
    new_matrix = np.zeros((h2, w2), dtype=np.int32)
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
    new_matrix = np.zeros((h2, w2), dtype=np.int32)
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

'''
Gray Level Converting Algorithm
'''
def convertGrayLevel(ori_img_matrix, ori_gray_level, new_gray_level):
    ori_pixel_range = 2 ** ori_gray_level
    new_pixel_range = 2 ** new_gray_level
    ratio = float(new_pixel_range) / float(ori_pixel_range)
    new_img_matrix = ori_img_matrix.copy()
    for row in range(len(ori_img_matrix)):
        for col in range(len(ori_img_matrix[row])):
            new_img_matrix[row][col] = int(ori_img_matrix[row][col] * ratio) * (256 / (2 ** new_gray_level))
    return new_img_matrix

'''
Histogram equalization algorithms
'''
def global_histogram_equalization(ori_img_matrix):
    intensity_count = np.zeros(256) 
    img_matrix = ori_img_matrix.copy()
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

def local_histogram_equalization(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    mid_val = int(mask_width * mask_height / 2.0)
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            cdf = [0] * 256 # cumulative distribution function (cdf)
            index = 0
            for x in range(mask_height):
                for y in range(mask_width):
                    # find the middle element in the window
                    if index == mid_val:
                        ele = padding_matrix[row + x, col + y]
                    pos = padding_matrix[row + x, col + y]
                    cdf[pos] += 1
                    index += 1
            # compute the cdf for the values in the window
            for i in range(1, 256):
                cdf[i] = cdf[i] + cdf[i-1]
            img_matrix[row][col] = int(cdf[ele] / (mask_width * mask_height) * 255.0)
    return img_matrix

'''
Spatial Filtering Algorithms
'''
def smoothing_filtering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            sum = 0
            for x in range(mask_height):
                for y in range(mask_width):
                    sum += padding_matrix[row + x][col + y]
            img_matrix[row][col] = int(sum / (mask_width * mask_height))
    return img_matrix

def median_filtering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    median_index = int(mask_width * mask_height / 2.0)
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            list = []
            for x in range(mask_height):
                for y in range(mask_width):
                    list.append(padding_matrix[row + x][col + y])
            list.sort()
            img_matrix[row][col] = list[median_index]
    return img_matrix

def sharpening_laplacian_filtering(ori_img_matrix, mask_width, mask_height):
    mid_val = int(mask_width * mask_height / 2.0)
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_val = 0
            index = 0
            for x in range(mask_height):
                for y in range(mask_width):
                    if index == mid_val:
                        new_val += padding_matrix[row + x][col + y] * (mask_width * mask_height - 1)
                    else:
                        new_val += padding_matrix[row + x][col + y] * -1
                    index += 1
            new_val += img_matrix[row][col]
            new_val = 255 if new_val > 255 else new_val
            new_val = 0 if new_val < 0 else new_val
            img_matrix[row][col] = new_val
    return img_matrix

def high_boosting_filtering(ori_img_matrix, mask_width, mask_height, K):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            sum = 0.0
            for x in range(mask_height):
                for y in range(mask_width):
                    sum += padding_matrix[row + x][col + y]
            sum /= (mask_width * mask_height)
            sum = (img_matrix[row][col] + K * (img_matrix[row][col] - sum))
            sum = 255 if sum > 255 else sum
            sum = 0 if sum < 0 else sum
            img_matrix[row][col] = sum
    return img_matrix

'''
Bit panel updating algorithm
'''
def update_bit_panel(ori_img_matrix, bit_mask):
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            img_matrix[row][col] &= bit_mask 
    return img_matrix

'''
Noise generating algorithms
'''
def gaussian(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    # TODO
    return img_matrix

def poisson(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    # TODO
    return img_matrix

def salt_and_pepper(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    # TODO
    return img_matrix

def speckle(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    # TODO
    return img_matrix

'''
Restoration Spatial filtering operations
'''
def arithmetic_mean_filtering(ori_img_matrix, mask_width, mask_height):
    print('arithmetic mean filtering')
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_value = 0.0
            for x in range(mask_height):
                for y in range(mask_width):
                    new_value += padding_matrix[row + x][col + y]
            new_value /= (mask_height * mask_width)
            img_matrix[row][col] = new_value
    return img_matrix

def geometric_mean_filtering(ori_img_matrix, mask_width, mask_height):
    print('geometric mean filtering')
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_value = 1.0
            for x in range(mask_height):
                for y in range(mask_width):
                    new_value *= padding_matrix[row + x][col + y]
            new_value **= float(1.0/(mask_height * mask_width))
            img_matrix[row][col] = new_value
    return img_matrix

def harmonic_mean_filtering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_value = 0.0
            for x in range(mask_height):
                for y in range(mask_width):
                    new_value += (1 / padding_matrix[row + x][col + y])
            new_value = (mask_height * mask_width) / new_value
            img_matrix[row][col] = new_value
    return img_matrix

def contraharmonic_mean_filtering(ori_img_matrix, mask_width, mask_height, q):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            up_sum = 0.0
            down_sum = 0.0
            for x in range(mask_height):
                for y in range(mask_width):
                    up_sum += padding_matrix[row + x][col + y] ** (q + 1)
                    down_sum += padding_matrix[row + x][col + y] ** q 
            if math.isnan(down_sum):
                down_sum = 0
            if math.isnan(up_sum / down_sum):
                new_value = 0
            else:
                new_value = up_sum / down_sum
            img_matrix[row][col] = new_value
    return img_matrix

def max_filtering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_value = -sys.maxsize
            for x in range(mask_height):
                for y in range(mask_width):
                    new_value = max(new_value, padding_matrix[row + x][col + y])
            img_matrix[row][col] = new_value
    return img_matrix

def min_filering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            new_value = sys.maxsize
            for x in range(mask_height):
                for y in range(mask_width):
                    new_value = min(new_value, padding_matrix[row + x][col + y])
            img_matrix[row][col] = new_value
    return img_matrix

def midpoint_filtering(ori_img_matrix, mask_width, mask_height):
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            max_num = 0
            min_num = 255
            for x in range(mask_height):
                for y in range(mask_width):
                    max_num = max(padding_matrix[row + x][col + y], max_num)
                    min_num = min(padding_matrix[row + x][col + y], min_num)
            new_value = min_num + (max_num - min_num) / 2;
            img_matrix[row][col] = new_value
    return img_matrix

def alpha_trimmed_mean_filtering(ori_img_matrix, mask_width, mask_height, p):
    print("alpha trimmed mean filter")
    padding_matrix = np.pad(ori_img_matrix, ((int(mask_height/2), int(mask_height/2)), (int(mask_width/2), int(mask_width/2))), 'constant')
    img_matrix = ori_img_matrix.copy()
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[0])):
            list = []
            for x in range(mask_height):
                for y in range(mask_width):
                    list.append(padding_matrix[row + x][col + y])
            list.sort()
            sum = 0
            for i in range(int(p/2), int(len(list)-p/2)):
                sum += list[i]
            new_value = float(1.0/(len(list)-p)) * sum
            img_matrix[row][col] = new_value
    return img_matrix

'''
Image compression algorithms
'''
def run_length_coding_on_grayscale_values(ori_img_matrix):
    start_time = time.time()
    vector = ori_img_matrix.flatten()
    counter = 1
    prev = vector[0]
    compressed_data = []
    for i in range(1, len(vector)):
        if vector[i] != prev:
            compressed_data.append(counter)
            compressed_data.append(prev)
            counter, prev = 1, vector[i]
        else:
            counter += 1
    compressed_data.append(counter)
    compressed_data.append(prev)
    end_time = time.time()
    compressed_data = np.array(compressed_data)
    compressed_data = compressed_data.astype(np.uint8)
    print("Compressed data: ", compressed_data)
    print("Compression time(RLC on Grayscale)", end_time - start_time)
    print("Size of original data: ", sys.getsizeof(ori_img_matrix))
    print("Size of compressed data: ", sys.getsizeof(compressed_data))
    np.savetxt("ori_rlc_gray.txt", compressed_data, fmt="%s")
    np.savetxt("compressed_rlc_gray.txt", ori_img_matrix, fmt="%s")
    return ori_img_matrix

def run_length_coding_on_bit_planes(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    print("run length bit planes")
    start_time = time.time()
    compressed_data = []
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    bit_panel_calculation(img_matrix, [], compressed_data)
    end_time = time.time()
    np.savetxt("compressed_rlc_bit.txt", compressed_data, fmt="%s")
    print("Compression time(RLC on Bitpanel)", end_time - start_time)
    print("Size of original data: ", sys.getsizeof(ori_img_matrix))
    print("Size of compressed data: ", sys.getsizeof(compressed_data))
    return ori_img_matrix

def bit_panel_calculation(img_matrix, bit_panel, compressed_data):
    target = 0
    counter = 0
    for row in range(len(img_matrix)):
        for col in range(len(img_matrix[row])):
            if (img_matrix[row][col] & target != 1):
                bit_panel.append(counter)
                target ^= 1
                counter = 0
            else:
                counter += 1
            img_matrix[row][col] >>= 1
    bit_panel.append(counter)
    compressed_data.append(bit_panel)


def variable_length_huffman_coding(ori_img_matrix):
    start_time = time.time()
    # 1.get probability
    frequency_array = [0] * 256
    for i in range(len(ori_img_matrix)):
        for j in range(len(ori_img_matrix[i])):
            frequency_array[ori_img_matrix[i][j]] += 1
    # 2.1 Create huffman nodes 
    node_array = []
    for i in range(len(frequency_array)):
        if frequency_array[i] != 0:
            node_array.append(HuffmanNode(frequency_array[i], i))
    node_array.sort(key=cmp_to_key(lambda node1, node2: -1 if node1.frequency < node2.frequency else 1))
    # 2.2 Build huffman tree
    while (len(node_array) != 1):
        smallest1 = node_array.pop(0)
        smallest2 = node_array.pop(0)
        new_node = HuffmanNode(smallest1.frequency + smallest2.frequency, -1)
        new_node.add_left(smallest1)
        new_node.add_right(smallest2)
        node_array.append(new_node)
        node_array.sort(key=cmp_to_key(lambda node1, node2: -1 if node1.frequency < node2.frequency else 1))
    # 3.1 Construct the encoding table from the huffman tree
    huffman_coding_dict = {}
    dfs(node_array[0], '', huffman_coding_dict)
    # 3.2 Convert the bit representation to interger
    for key in huffman_coding_dict:
        string_number = int(huffman_coding_dict[key], 2)
        huffman_coding_dict[key] = string_number
    print(huffman_coding_dict)
    # 4. Convert original image using the encoding table
    encoded_image = ori_img_matrix.copy()
    for row in range(len(encoded_image)):
        for col in range(len(encoded_image[0])):
            encoded_image[row][col] = huffman_coding_dict[encoded_image[row][col]]
    end_time = time.time()
    print(ori_img_matrix)
    print(encoded_image)
    # 6. Time and Size analysis
    print(f"Time used: {end_time - start_time}")
    ori_size = 0
    for row in range(len(ori_img_matrix)):
        for col in range(len(ori_img_matrix[0])):
            value = ori_img_matrix[row][col]
            while value:
                ori_size += 1
                value >>= 1
    print(f"Original size: {ori_size}")
    compressed_size = 0
    for row in range(len(encoded_image)):
        for col in range(len(encoded_image[0])):
            value = encoded_image[row][col]
            while value:
                compressed_size += 1
                value >>= 1
    print(f"Compressed size: {compressed_size}")
    print(f"Compression ratio: {ori_size / compressed_size}")
    # 7. Save original and comporesss representation of the images in txt files
    huffman_coding_matrix = []
    for key in huffman_coding_dict:
        huffman_coding_matrix.append([key, huffman_coding_dict[key]])
    huffman_coding_matrix.sort(key=cmp_to_key(lambda p1, p2: -1 if p1[0] < p2[0] else 1))
    np.savetxt("./huffman/huffman_map.txt", huffman_coding_matrix, fmt="%s")
    np.savetxt("./huffman/huffman_original.txt", ori_img_matrix, fmt="%s")
    np.savetxt("./huffman/huffman_compressed.txt", encoded_image, fmt="%s")
    return ori_img_matrix

def dfs(huffman_node, encode, huffman_coding_dict):
    if not huffman_node:
        return
    if huffman_node.left is None and huffman_node.right is None:
        # huffman_coding_dict.append([huffman_node.value, encode])
        huffman_coding_dict[huffman_node.value] = encode
    dfs(huffman_node.left, encode + '0', huffman_coding_dict)
    dfs(huffman_node.right, encode + '1', huffman_coding_dict)

class HuffmanNode:
    def __init__(self, frequency, value):
        self.frequency = frequency
        self.value = value
        self.left = None
        self.right = None
    
    def add_left(self, child):
        self.left = child
    
    def add_right(self, child):
        self.right = child

def lzw(ori_img_matrix):
    img_matrix = ori_img_matrix.copy()
    col_length = len(ori_img_matrix[0])
    total_length = len(ori_img_matrix) * len(ori_img_matrix[0])
    print("lzw")
    # 1. Build the original dictionary
    encoding_dictionary = {}
    compressed_data = []
    next_value = 256
    # 2. Iterate the image and build the dictionary
    start_time = time.time()
    valid_start_index = 0
    valid_end_index = 0
    while valid_end_index < total_length:
        next_start_index = valid_end_index
        next_end_index = next_start_index
        valid_array = []
        new_array = []
        for i in range(next_start_index, next_end_index):
            valid_array.append(ori_img_matrix[i / col_length][i % col_length])
            new_array.append(ori_img_matrix[i / col_length][i % col_length])
        compressed_data.append(encoding_dictionary[valid_array])
        encoding_dictionary[new_array] = next_value
        next_value += 1
    end_time = time.time()
    # 3. Time and Size Analysis
    print(f"Time used: {end_time - start_time}")
    ori_size = sys.size_of(ori_img_matrix)
    compressed_size = sys.size_of(compressed_data)
    print(f"Compressed size: {compressed_size}")
    print(f"Compression ratio: {ori_size / compressed_size}")
    # 4. Save compressed data
    np.savetxt("./lzw/lzw_compressed.txt", compressed_data, fmt="%s")
    return img_matrix
