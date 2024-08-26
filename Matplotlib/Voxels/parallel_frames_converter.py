from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from random import randint


from matplotlib import colormaps
cmaps = list(colormaps)

def process_frame(frame_index, Z):
    image_path = 'frames/frame_' + str(frame_index) + '.jpg' # <-- Path to load images
    image = Image.open(image_path)
    pixel_array = np.array(image)

    indx = (frame_index // 38) % 170

    height, width, channels = pixel_array.shape

    step = 25 # <-- This is sampling step value

    height = height // step
    width = width // step

    data = [[[0 for _1 in range(height + width)] for _2 in range(height)] for _3 in range(width)]
    colors = [[[(0, 0, 0) for _1 in range(height + width)] for _2 in range(height)] for _3 in range(width)] 

    for i in range(width):

        for j in range(height):

            col = pixel_array[j * step, i * step]

            indx = randint(0, width + height)

            colors[i][height - j - 1][indx - 1] = col / 255

            data[i][height - j - 1][indx - 1] = 1

    data = np.array(data)
    colors = np.array(colors)

    fig = plt.figure(figsize=(10, 10))

    ax1 = fig.add_subplot(111, projection='3d')
    ax1.voxels(data, facecolors=colors)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    ax1.set_zticks([0, 0, 0])

    ax1.view_init(elev=90, azim=-90)

    fig.savefig('frames_new/frame_' + str(frame_index) + '.jpeg', dpi=300) # <-- Path to save images

    plt.clf()

    ax2 = fig.add_subplot(111, projection='3d')
    ax2.voxels(data, facecolors=colors)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    ax2.view_init(elev=45, azim=-135)

    fig.savefig('frames_new1/frame_' + str(frame_index) + '.jpeg', dpi=300) # <-- Path to save images

    plt.clf()

    plt.close(fig)
    
    print("Frame " + str(frame_index) + " was created.")


def convert_parallel(start_frame, finish_frame, Z):
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)  # Create a pool of processes

    # Map the frames to be processed by the pool of processes
    pool.map(process_frame, range(start_frame, finish_frame + 1), Z)

    pool.close()
    pool.join()


if __name__ == '__main__':
    convert_parallel(5500, 6571) # <-- Start and finish frames
    print('Done')
