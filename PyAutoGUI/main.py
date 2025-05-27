import pyautogui
import numpy as np
from PIL import Image

from typing import Tuple


class PaintPrinter:
    """Класс отрисовки кадров в MS Paint и их сохранения.

    Использует Pyautogui что бы управлять нажатиями. Отрисовывает их и сохраняте в формате frame_{index}.jpg.

    Attributes:
        input_dir (str): Путь до папки с изображениями. 
        output_dir_dir (str): Путь до папки для сохранения изображений.
        frame_range (Tuple[int, int]): Диапазон кадров для генерации.
        rect (Tuple[int, int, int, int]): Границы холста. 
        step (int): Шаг дискретизации. 
        delay (float): Задержка между вводом.
    
    """
    def __init__(self, input_dir: str, output_dir: str, frame_range: Tuple[int, int], 
                 rect: Tuple[int, int, int, int], step: int = 5, delay: float = 0.01) -> None:
        """Инициализирует класс для отрисовки.
        
        Args:
            input_dir (str): Путь до папки с изображениями. 
            output_dir_dir (str): Путь до папки для сохранения изображений. 
            frame_range (Tuple[int, int]): Диапазон кадров для генерации. 
            rect (Tuple[int, int, int, int]): Границы холста. 
            step (int): Шаг дискретизации. 
            delay (float): Задержка между вводом.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.rect = rect
        self.delay = delay
        self.step = step
        self.frame_range = frame_range

    def process_frame(self, pixel_array: np.ndarray) -> None:
        """Обработка одного кадра

        Args:
            pixel_array (np.ndarray): Массив цветов изображения.
        """
        height, width = pixel_array.shape[0], pixel_array.shape[1]

        height = height // self.step
        width = width // self.step

        mouse_down = False

        for x in range(width):
            for y in range(height):
                # Проверяем, является ли пиксель черным
                if pixel_array[y * self.step, x * self.step][0] < 125:
                    target_x = self.rect[0] + x * self.step
                    target_y = self.rect[1] + y * self.step
                    
                    # Если мышь не нажата - нажимаем
                    if not mouse_down:
                        pyautogui.mouseDown(x=target_x, y=target_y)
                        mouse_down = True
                    # Если предыдущий пиксель был рядом - рисуем линию
                    elif last_x is not None and abs(target_x - last_x) <= self.step and abs(target_y - last_y) <= self.step:
                        pyautogui.moveTo(target_x, target_y)
                    # Если разрыв - отпускаем и снова нажимаем
                    else:
                        pyautogui.mouseUp()
                        pyautogui.mouseDown(x=target_x, y=target_y)
                    
                    last_x, last_y = target_x, target_y
                else:
                    # Если пиксель не черный и кнопка нажата - отпускаем
                    if mouse_down:
                        pyautogui.mouseUp()
                        mouse_down = False
                        last_x, last_y = None, None

            # Отпускаем кнопку мыши в конце
            if mouse_down:
                pyautogui.mouseUp()

    def clean_canvas(self) -> None:
        """Очищает холст, рисуя белый прямоугольник по границам rect."""
        # Выбираем инструмент "Прямоугольник"
        pyautogui.click(x=634, y=80)  
        pyautogui.sleep(self.delay)

        # Рисуем прямоугольник
        pyautogui.mouseDown(x=self.rect[2], y=self.rect[3])
        pyautogui.dragTo(x=self.rect[0] - 10, y=self.rect[1] - 10, duration=0.25)
        pyautogui.mouseUp()
        pyautogui.sleep(self.delay)

        # Возвращаем инструмент "Карандаш"
        pyautogui.click(x=400, y=88)
        pyautogui.sleep(self.delay)

    def render(self):
        """Выделяет изображение для прогрузки"""
        # Выбираем инструмент "Выделение"
        pyautogui.click(x=213, y=88)  
        pyautogui.sleep(self.delay)

        # Выделяем
        pyautogui.mouseDown(x=self.rect[2], y=self.rect[3])
        pyautogui.dragTo(x=self.rect[0] - 10, y=self.rect[1] - 10, duration=0.25)
        pyautogui.mouseUp()
        pyautogui.sleep(self.delay)

        # Возвращаем инструмент "Карандаш"
        pyautogui.click(x=400, y=88)
        pyautogui.sleep(5 * self.delay)

    def save_frame(self, idx: int) -> None:
        """Делает снимок экрана и сохраняет в output_dir
        
        Args:
            idx (int): Номер обрабатываемого кадра.
        """
        screenshot = pyautogui.screenshot()
        screenshot.save(self.output_dir + f'/frame_{idx}.jpg')

    def run(self) -> None:
        """Обрабатывает изображения из input_folder и сохраняет в output_folder.
        """
        pyautogui.PAUSE = 0
        pyautogui.alert(f'Start?')

        for idx in range(*self.frame_range):  
            image = Image.open(self.input_dir + f"/frame_{idx}.jpg")
            pixel_array = np.array(image)
            self.process_frame(pixel_array)
            pyautogui.sleep(0.1)
            self.render()
            self.save_frame(idx)
            self.clean_canvas()


if __name__ == '__main__':
    app = PaintPrinter(input_dir='frames', output_dir='output', frame_range=(0, 6572), 
                       rect=(15 + 350, 185 + 15, 985 + 360, 917 + 20), delay=0.01, step=3)
    app.run()
