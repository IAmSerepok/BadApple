from PIL import Image
import numpy as np
import multiprocessing


def process_frame(frame_index):
    image_path = f'frames/frame_{frame_index}.jpg'  # <-- Path to Bad Apple frames
    image = Image.open(image_path)
    pixel_array = np.array(image)

    height, width, channels = pixel_array.shape

    np.random.seed(42)
    noise_bgr = np.random.random((width, height))
    np.random.seed(42 + frame_index)
    noise = np.random.random((width, height))

    for x in range(width):
        for y in range(height):

            r, g, b = pixel_array[y, x]
            value = noise_bgr[x, y]
            if (r > 230) and (g > 230) and (b > 230):
                value = noise[x, y]

            value = int(np.interp(value, [0, 1], [0, 255]))

            image.putpixel((x, y), (value, value, value))

    image.save('frames_new/frame_' + str(frame_index) + '.jpeg')
    
    print("Frame " + str(frame_index) + " was created.")


def convert_parallel(start_frame, finish_frame):
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)  # Create a pool of processes

    # Map the frames to be processed by the pool of processes
    pool.map(process_frame, range(start_frame, finish_frame + 1))

    pool.close()
    pool.join()


if __name__ == '__main__':
    convert_parallel(5499, 6572)  # <-- Start and finish frames
    print('Done')
