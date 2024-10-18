import sys
import os
import random

def truncater(input_filename, output_filename):
    with open(input_filename, 'rb') as f:
        data = f.read()

    if len(data) <= 64:
        print("The file is too small to truncate 16 bytes while avoiding the first 32 bytes.")
        return

    start_range = 32
    end_range = len(data) - 16

    remove_position = random.randint(start_range, end_range - 1)

    truncated_data = data[:remove_position] + data[remove_position + 16:]

    with open(output_filename, 'wb') as f:
        f.write(truncated_data)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 truncater.py <input_filename> <output_filename>")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        truncater(input_filename, output_filename)