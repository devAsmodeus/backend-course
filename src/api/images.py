from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_file(file: UploadFile):
    ImagesService().upload_image(file)
