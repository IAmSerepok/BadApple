from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing


def process_frame(frame_index):
    image_path = 'frames/frame_' + str(frame_index) + '.jpg' # <-- Path to load images
    image = Image.open(image_path)
    pixel_array = np.array(image)

    height, width, channels = pixel_array.shape

    step = 3 # <-- This is sampling step value

    height = height // step
    width = width // step

    x_data = []
    y_data = []

    for i in range(width):

        for j in range(height):

            col = pixel_array[j * step, i * step]

            v = 0
            for _1 in range(10, 240, 10):
                if col[0] < _1:
                    v += 1

            for _ in range(v):
                x_data.append(i * step)
                y_data.append(pixel_array.shape[0] - j * step)

    my_bins = ([_1 * step for _1 in range(width)], [_2 * step for _2 in range(height)])

    plt.subplots(figsize=(9, 7)) # image size

    plt.hist2d(x_data, y_data, bins=my_bins, cmap='Greys', vmax=25)

    plt.colorbar()

    plt.savefig('frames_new/frame_' + str(frame_index) + '.jpeg', dpi=300) # <-- Path to save images

    plt.close()
    
    print("Frame " + str(frame_index) + " was created.")


def convert_parallel(start_frame, finish_frame):
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)  # Create a pool of processes

    # Map the frames to be processed by the pool of processes
    pool.map(process_frame, range(start_frame, finish_frame + 1))

    pool.close()
    pool.join()


if __name__ == '__main__':
    convert_parallel(6000, 6571) # <-- Start and finish frames
    print('Done')
