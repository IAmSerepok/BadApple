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
    space = 0 # <-- This is space between bars value
    is_colored = False # <-- Display in color?
    width = width // step

    sost = []
    for i in range(width):
        if pixel_array[0, i * step][0] > 100:
            sost.append('black')
        else:
            sost.append('white')

    data = [[], []]

    for i in range(0, width, step):

        h = 1

        for j in range(height - 1, -1, -1):

            new_sost = 'white'
            
            if pixel_array[j, i * step][0] > 100:
                new_sost = 'black'

            if sost[i] != new_sost:

                delta = 0

                if new_sost == 'white':
                    delta = 1

                sost[i] = new_sost

                try:
                    data[2*h+delta].append(i * step)

                except:
                    for _ in range(2):
                        data.append([])

                    data[2*h+delta].append(i * step)

                h += 1
        
            else:

                delta = 0

                if new_sost == 'white':
                    delta = 1

                data[2*(h-1)+delta].append(i * step)

    my_bins = [i * step for i in range(width + 1)]

    colors = ['white', 'black'] * (len(data) // 2)

    plt.figure(figsize=(9, 7))

    if is_colored:
        plt.hist(data, bins=my_bins, stacked=True, width=step**2 - space)
    else:
        plt.hist(data, bins=my_bins, stacked=True, width=step**2 - space, color=colors)

    plt.savefig('frames_gray_border/frame_' + str(frame_index) + '.jpeg', dpi=300) # <-- Path to save images

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
