import cv2
import os


def video_to_frame(video_path: str, output_dir: str) -> int:
    """Извлекает все кадры из видеофайла и сохраняет их как отдельные изображения.

    Функция принимает путь к видеофайлу и директорию для сохранения кадров.
    Кадры сохраняются в формате JPG с именами в формате 'frame_0.jpg', 'frame_1.jpg' и т.д.

    Args:
        video_path (str): Абсолютный или относительный путь к исходному видеофайлу.
                   Поддерживаемые форматы: .mp4, .avi, .mov и другие, которые может
                   прочитать OpenCV.
        output_dir (str): Директория для сохранения извлечённых кадров. Будет создана,
                   если не существует.

    Returns:
        frames_count (int): Количество успешно сохранённых кадров.

    Raises:
        FileNotFoundError: Если видеофайл не существует.
        cv2.error: Если возникла ошибка OpenCV при чтении видео.
        OSError: Если невозможно создать директорию для сохранения кадров.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Видеофайл не найден: {video_path}")

    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise cv2.error(f"Не удалось открыть видеофайл: {video_path}")

        os.makedirs(output_dir, exist_ok=True)

        frame_count = 0
        while True:
            success, image = video.read()
            if not success:
                break

            frame_file = os.path.join(output_dir, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_file, image)
            frame_count += 1

        return frame_count

    finally:
        if 'video' in locals():
            video.release()
