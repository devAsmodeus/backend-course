import os

from PIL import Image
from time import sleep
from pathlib import Path

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_tasks():
    sleep(5)
    return 'Я поработал где зарплата'


@celery_instance.task
def resize_image(image_path: str):
    image_path = Path(image_path)
    sizes = [1000, 500, 200]
    output_folder = image_path.parent
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")
