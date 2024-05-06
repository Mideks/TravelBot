import os

from PIL import Image


def compress_image_if_needed(image_path, max_size=1024, quality=85):
    """
    Сжимает изображение, если его размер превышает max_size, сохраняя исходное изображение без изменений.

    :param image_path: Путь к исходному изображению.
    :param max_size: Максимальный размер изображения в пикселях.
    :param quality: Качество сжатия для JPEG (от 1 до 100).
    """
    # Открываем изображение
    img = Image.open(image_path)

    # Проверяем, нужно ли изменять размер изображения
    if img.size[0] > max_size or img.size[1] > max_size:
        # Изменяем размер изображения
        img.thumbnail((max_size, max_size))

        # Сохраняем изображение с новым качеством
        img.save(image_path, "JPEG", quality=quality)
        print(f"{image_path} сжато")


def process_images_in_folder(folder_path, max_size=1024, quality=85):
    """
    Обрабатывает все изображения в указанной папке, сжимая те, которые слишком большие.

    :param folder_path: Путь к папке с изображениями.
    :param max_size: Максимальный размер изображения в пикселях.
    :param quality: Качество сжатия для JPEG (от 1 до 100).
    """
    # Проверяем, существует ли указанная папка
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не найдена.")
        return

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        # Проверяем, является ли файл изображением
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            compress_image_if_needed(image_path, max_size, quality)


# Пример использования
process_images_in_folder("../data/media_old", max_size=1024, quality=85)