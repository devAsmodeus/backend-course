from datetime import date
from fastapi import HTTPException


class HasBookedException(Exception):
    detail = 'External exception'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HasBookedException):
    detail = 'Object not found'


class ObjectAlreadyExistsException(HasBookedException):
    detail = 'Object already exists'


class RoomCannotBeBookedException(HasBookedException):
    detail = 'Current room cannot be booked'


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail='Дата заезда не может быть позже даты выезда')


class HasBookedHTTPException(HTTPException):
    status_code = 500
    detail = 'External exception'

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class HotelNotFoundHTTPException(HasBookedHTTPException):
    status_code = 404
    detail = 'Hotel not found'


class RoomNotFoundHTTPException(HasBookedHTTPException):
    status_code = 404
    detail = 'Room not found'
