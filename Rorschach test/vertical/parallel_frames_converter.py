from PIL import Image
import numpy as np
import multiprocessing


def process_frame(frame_index):
    image_path = 'frames1/frame_' + str(frame_index) + '.jpeg' # <-- Path to load images
    image = Image.open(image_path)
    pixel_array = np.array(image)

    height, width, channels = pixel_array.shape

    for x in range(width):

        for y in range(height):
            
            r, g, b = pixel_array[y, x]
            r0, g0, b0 = pixel_array[y, width - x - 1]

            if r0 < 30:
                image.putpixel((x, y), (255 - r, 255 - g, 255 - b))

    image.save('frames1_new/frame_' + str(frame_index) + '.jpeg')

    print("Frame " + str(frame_index) + " was created.")


def convert_parallel(start_frame, finish_frame):
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)  # Create a pool of processes

    # Map the frames to be processed by the pool of processes
    pool.map(process_frame, range(start_frame, finish_frame + 1))

    pool.close()
    pool.join()


if __name__ == '__main__':
    convert_parallel(1000, 6571) # <-- Start and finish frames
    print('Done')
