class HasBookedException(Exception):
    detail = 'External exception'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(HasBookedException):
    detail = 'Object not found'


class RoomCannotBeBookedException(HasBookedException):
    detail = 'Current room cannot be booked'
