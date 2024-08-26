from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing


def process_frame(frame_index):
    image_path = 'frames/frame_' + str(frame_index) + '.jpg' # <-- Path to load images
    image = Image.open(image_path)
    pixel_array = np.array(image)

    height, width, channels = pixel_array.shape

    step = 10 # <-- This is sampling step value

    height = height // step
    width = width // step

    plt.subplots(figsize=(9, 7)) # image size

    plt.xlim(0, 960)
    plt.ylim(0, 720)

    for i in range(width):

        j = 0

        data_x = []
        data_y = []

        while j < height:

            col = pixel_array[j * step, i * step]

            if np.all(col < 20):

                data_x.append(i * step)
                data_y.append(pixel_array.shape[0] - j * step)

            else:

                plt.plot(data_x, data_y, color='black', linewidth=4.5)

                data_x = []
                data_y = []
            
            j += 1

        plt.plot(data_x, data_y, color='black', linewidth=4.5)

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
    convert_parallel(5000, 6571) # <-- Start and finish frames
    print('Done')
