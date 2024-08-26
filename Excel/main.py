import xlwings as xw
from PIL import Image
import numpy as np
from PIL import ImageGrab


def number_to_column(num):
    """Convert number to Excel char index"""
    result = ''
    while num:
        num, remainder = divmod(num - 1, 26)
        result = chr(65 + remainder) + result
    return result


def get_shape(frame_path):
    
    image = Image.open(frame_path)

    pixel_array = np.array(image)

    height, width, channels = pixel_array.shape

    step = 25  # Sampling step value

    width, height = width // step, height // step

    colors = pixel_array[::step, ::step]

    return width, height, step, colors


def print_frame(sheet, frame_path, indx):

    width, height, step, colors = get_shape(frame_path)

    for i in range(1, width + 1):
        for j in range(1, height + 1):
            col = colors[j - 1, i - 1]
            if col.any() < 250: 
                sheet.range(number_to_column(i) + str(j + indx * height)).color = col

    print(frame_path)


def create_frames(start_frame, end_frame):
    """Print frames in 'tmp'"""

    wb = xw.books.active
    sheet_tmp = wb.sheets['tmp']  # Second page title
    
    for indx in range(start_frame, end_frame + 1):
        
        image_path = 'frames/frame_' + str(indx) + '.jpg'  # Forming path to frame

        print_frame(sheet_tmp, image_path, indx)
        

def get_source_range(indx, width, height):
    """Get frame from 'tmp'"""
    return (number_to_column(1) + str(1 + indx * height) + ':' 
            + number_to_column(width) + str((indx + 1) * height))


def save_frame(indx):
    screenshot = ImageGrab.grab(bbox=(0, 0, 1920, 1000))
    screenshot.save('frames_new/frame_' + str(indx) + '.jpg') # Path to save frames


def play(start_frame, end_frame):
    """Play created in 'tmp' frames in 'Sheet'"""
    
    wb = xw.books.active
    sheet = wb.sheets['Sheet']  # Main page title
    sheet_tmp = wb.sheets['tmp']  # Second page title
    
    delta = (3, 5)

    for indx in range(start_frame, end_frame + 1):

        width, height, step, colors = get_shape('frames/frame_0.jpg')

        source_range = sheet_tmp.range('tmp!' + get_source_range(indx, width, height))
        target_range = sheet.range(number_to_column(1 + delta[1]) + str(1 + delta[0]))

        source_range.options(index=False, header=False).copy(destination=target_range)

        sheet.range('A225').value = 'Frame number ' + str(indx + 1) + '.'

        # save_frame(indx)


# create_frames(0, 6572)
# play(900, 6571)
