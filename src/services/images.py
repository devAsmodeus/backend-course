import shutil

from fastapi import UploadFile
from pathlib import Path

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):

    def upload_image(self, file: UploadFile):
        image_path = Path(__file__).parent.parent / "static" / "images" / file.filename
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(str(image_path))
