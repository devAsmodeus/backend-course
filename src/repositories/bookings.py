from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingsAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingsAdd
