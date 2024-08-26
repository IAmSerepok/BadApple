from PIL import Image
import numpy as np
from random import randint
from copy import deepcopy
from time import time


folder = 'frames/' # <-- Path to Bad Apple frames folder
start_frame, end_frame = 0, 6571 # <-- Frames interval
step = 4 # <-- Sampling step

image = Image.open(folder + f'frame_{0}.jpg')

start_time = time()

pixel_array = np.array(image)
height, width, channels = pixel_array.shape
colls, rows = width // step, height // step

field = [[randint(0, 2) for _2 in range(- step, height + step, step)] for _1 in range(- step, width + step, step)]


def check_cell(color, x, y):
    global field
    count = 0
    prev_col = color
    col = (color + 1) % 3
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if field[i][j] == col:
                count += 1
    if count >= 3:
        return col
    else:
        return prev_col
        

def iter():
    global field
    new_field = [[0 for _2 in range(- step, height + step, step)] for _1 in range(- step, width + step, step)]
    for x in range(1, colls + 1):
        for y in range(1, rows + 1):
            new_field[x][y] = check_cell(field[x][y], x, y)
    field = deepcopy(new_field)


for _1 in range(15):
        iter()


for _ in range(start_frame, end_frame + 1):

    iter()

    image = Image.open(folder + f'frame_{_}.jpg')

    pixel_array = np.array(image)

    res = Image.new('RGB', (width, height), (160, 90, 170))

    for x in range(1, colls + 1):
        for y in range(1, rows + 1):
            if pixel_array[(y - 1) * step, (x - 1) * step][0] > 235:
                if field[x][y] == 1:
                    for i in range(x * step - step, x * step):
                        for j in range(y * step - step, y * step):
                            res.putpixel((i, j), (150, 190, 220))
                elif field[x][y] == 2:
                    for i in range(x * step - step, x * step):
                        for j in range(y * step - step, y * step):
                            res.putpixel((i, j), (235, 150, 150))

    res.save(f'output/frame_{_}.jpg') # <-- Saving image
    print(f'Frame {_} created')

print(f'All frames created in {time() - start_time} seconds')
