from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from random import randint


from matplotlib import colormaps
cmaps = list(colormaps)

def process_frame(frame_index):
    image_path = 'frames/frame_' + str(frame_index) + '.jpg' # <-- Path to Bad Apple frames
    image = Image.open(image_path)
    pixel_array = np.array(image)

    bgr = Image.open('ric/frame_' + str(frame_index) + '.jpg') # <-- Path to Rick Roll frames
    bgr = bgr.crop((0, 0, 960, 720)) # <-- Crop bgr frame
    bgr_pixel_array = np.array(bgr)

    height, width, channels = pixel_array.shape

    for x in range(width):

        for y in range(height):
            
            r, g, b = pixel_array[y, x]

            if (r > 230) and (g > 230) and (b > 230):
                r, g, b = bgr_pixel_array[y, x]
                bgr.putpixel((x, y), (255 - r, 255 - g, 255 - b))

    bgr.save('frames_new/frame_' + str(frame_index) + '.jpeg')
    
    print("Frame " + str(frame_index) + " was created.")


def convert_parallel(start_frame, finish_frame):
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)  # Create a pool of processes

    # Map the frames to be processed by the pool of processes
    pool.map(process_frame, range(start_frame, finish_frame + 1))

    pool.close()
    pool.join()


if __name__ == '__main__':
    convert_parallel(0, 6571) # <-- Start and finish frames
    print('Done')
