import cv2
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

input_dir = 'frames'
output_dir = 'output'
extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')


def process_image(args):
    """Обрабатывает одно изображение. Возвращает (filename, status, message)."""
    filename, input_dir, output_dir = args
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return filename, 'skip', f'не удалось прочитать: {input_path}'

    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    grad_mag = np.uint8(np.clip(grad_mag, 0, 255))

    ok = cv2.imwrite(output_path, grad_mag)
    if not ok:
        return filename, 'error', f'не удалось записать: {output_path}'
    return filename, 'ok', output_path


def main():
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in sorted(os.listdir(input_dir))
             if f.lower().endswith(extensions)]

    if not files:
        return

    tasks = [(f, input_dir, output_dir) for f in files]

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, t): t[0] for t in tasks}

        done = 0
        total = len(futures)
        for future in as_completed(futures):
            filename = futures[future]
            try:
                name, status, msg = future.result()
                done += 1
                print(f"[{done}/{total}] {status:5s} {name} -> {msg}")
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")


if __name__ == '__main__':
    main()
