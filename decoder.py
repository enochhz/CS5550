import time
import numpy as np

def run_length_gray_decoding(compressed_data_file, output_file):
    decoded_data = []
    start_time = time.time()
    with open(compressed_data_file) as file:
        while True:
            odd_line = file.readline()
            even_line = file.readline()
            if odd_line and even_line:
                frequency = int(odd_line.replace('\n', ''))
                number = even_line.replace('\n', '')
                for i in range(frequency):
                    decoded_data.append(number)
            else:
                break
    end_time = time.time()
    print(f"Decoding (run length gray) Time used: {end_time - start_time}")
    np.savetxt(output_file, decoded_data, fmt="%s")

run_length_gray_decoding('./run_length/compressed_rlc_gray.txt', './run_length/decoded_gray.txt')

def run_length_bit_decoding(compressed_data_file, output_file):
    decoded_data = []
    start_time = time.time()
    with open(compressed_data_file) as file:
        for line in file:
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('\n', '')
            numbers = line.split(', ')
            next_bit = 0
            index = 0
            for num in numbers:
                for i in range(int(num)):
                    if len(decoded_data) < index + 1:
                        decoded_data.append(1)
                        decoded_data[index] &= next_bit
                    else:
                        decoded_data[index] <<= 1
                        decoded_data[index] ^= (next_bit ^ 1)
                    index += 1
                next_bit ^= 1
    end_time = time.time()
    print(f"Decoding (run length bit) Time used: {end_time - start_time}")
    np.savetxt(output_file, decoded_data, fmt="%s")

run_length_bit_decoding('./run_length/compressed_rlc_bit.txt', './run_length/decoded_bit.txt')

def huffman_decoding(compressed_data_file, dictionary_file, output_file):
    start_time = time.time()
    decoding_dictionary = {}
    with open(dictionary_file) as file:
        for line in file:
            key, value = line.strip().split(' ', 1)
            decoding_dictionary[value] = key
    decoded_data = []
    with open(compressed_data_file) as file:
        new_row = []
        for line in file:
            line = line.replace('\n', '')
            numbers = line.split(' ')
            for num in numbers:
                new_row.append(decoding_dictionary[num])
        decoded_data.append(new_row)
    end_time = time.time()
    print(f"huffman decoding-Time used: {end_time - start_time}")
    np.savetxt(output_file, decoded_data, fmt="%s")

huffman_decoding("./huffman/huffman_compressed.txt", "./huffman/huffman_map.txt", "./huffman/huffman_decoded_data.txt")

def lzw_decoding(compressed_data_file, dictionary_file, output_file):
    start_time = time.time()
    decoding_dictionary = {}
    with open(dictionary_file) as file:
        for line in file:
            numbers, code = line.strip().split('] ', 1)
            numbers = numbers.replace('[', '')
            numbers = numbers.replace(',', '')
            numbers = numbers.split(' ')
            decoding_dictionary[code] = numbers
    decoded_data = []
    with open(compressed_data_file) as file:
        for line in file:
            index = line.replace('\n', '')
            decoded_data.extend(decoding_dictionary[index])
    end_time = time.time()
    print(f"lzw decoding-Time used: {end_time - start_time}")
    np.savetxt(output_file, decoded_data, fmt="%s")

lzw_decoding('./lzw/lzw_compressed.txt', './lzw/lzw_encoding_dictionary.txt', './lzw/decoded_data.txt')