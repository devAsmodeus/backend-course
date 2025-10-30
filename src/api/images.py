import shutil

from pathlib import Path
from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_file(
    file: UploadFile,
):
    image_path = Path(__file__).parent.parent / "static" / "images" / file.filename
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(str(image_path))
