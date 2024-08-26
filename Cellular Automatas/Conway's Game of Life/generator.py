from PIL import Image
import numpy as np
from random import random
from copy import deepcopy
from time import time


folder = 'frames/' # <-- Path to Bad Apple frames folder
start_frame, end_frame = 0, 6571 # <-- Frames interval
step = 5 # <-- Sampling step

rule_b = [3]
rule_s = [2, 3]

image = Image.open(folder + f'frame_{0}.jpg')

start_time = time()

pixel_array = np.array(image)
height, width, channels = pixel_array.shape
colls, rows = width // step, height // step

field = [[1 if random() < 0.3 else 0 for _2 in range(- step, height + step, step)] for _1 in range(- step, width + step, step)]


def check_cell_mur(x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if field[i][j]:
                count += 1

    if field[x][y]:
        count -= 1
        if count in rule_s:
            return 1
        return 0
    else:
        if count in rule_b:
            return 1
        return 0
        

def iter():
    new_field = [[0 for _2 in range(- step, height + step, step)] for _1 in range(- step, width + step, step)]
    for x in range(1, colls + 1):
        for y in range(1, rows + 1):
            new_field[x][y] = check_cell_mur(x, y)
    global field
    field = deepcopy(new_field)


for _1 in range(15):
        iter()


for _ in range(start_frame, end_frame + 1):

    iter()

    image = Image.open(folder + f'frame_{_}.jpg')

    pixel_array = np.array(image)

    res = Image.new('RGB', (width, height), (0, 0, 0))

    for x in range(1, colls + 1):
        for y in range(1, rows + 1):
            if (pixel_array[(y - 1) * step, (x - 1) * step][0] > 235) and field[x][y]:
                for i in range(x * step - step, x * step):
                    for j in range(y * step - step, y * step):
                        res.putpixel((i, j), (255, 255, 255))
            elif random() < 0.01:
                field[x][y] = 1

    res.save(f'output/frame_{_}.jpg') # <-- Saving image
    print(f'Frame {_} created')

print(f'All frames created in {time() - start_time} seconds')
