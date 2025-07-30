from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(default=5, description="Количество отелей на странице", ge=1, le=10)]


PaginationDep = Annotated[PaginationParams, Depends()]
