import os

from PIL import Image
from typing import Dict


def crop_images(input_dir: str, output_dir: str, rect: Dict[int, int, int, int]) -> None:
    """
    Обрезает все изображения в указанной директории по заданному прямоугольнику и сохраняет в новую директорию.

    Функция обрабатывает все изображения форматов: .png, .jpg, .jpeg, .bmp в input_dir.
    Результат сохраняется в output_dir с префиксом 'cropped_' в имени файла.

    Args:
        input_dir (str): Путь к директории с исходными изображениями.
        output_dir (str): Путь к директории для сохранения результатов (будет создана, если не существует).
        rect (Dict[int, int, int, int]): Координаты области обрезки в формате (left, upper, right, lower).

    Raises:
        ValueError: Если координаты rect некорректны (left >= right или upper >= lower).
        OSError: Если input_dir не существует или недоступен.
    """
    # Валидация координат обрезки
    if rect[0] >= rect[2] or rect[1] >= rect[3]:
        raise ValueError(
            f"Некорректные координаты обрезки: {rect}. "
            "Должно быть left < right и upper < lower."
        )

    # Проверка существования входной директории
    if not os.path.exists(input_dir):
        raise OSError(f"Директория {input_dir} не существует или недоступна")

    # Создание выходной директории (если не существует)
    os.makedirs(output_dir, exist_ok=True)

    # Обработка каждого файла в директории
    for filename in os.listdir(input_dir):
        # Проверка расширения файла
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            try:
                # Полный путь к файлу
                img_path = os.path.join(input_dir, filename)
                
                # Открытие изображения
                with Image.open(img_path) as img:
                    # Обрезка изображения
                    cropped_img = img.crop(rect)
                    
                    # Сохранение результата
                    output_path = os.path.join(output_dir, f"cropped_{filename}")
                    cropped_img.save(output_path)
                    
                    print(f"Изображение {filename} обрезано и сохранено как {output_path}")
                    
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {str(e)}")
