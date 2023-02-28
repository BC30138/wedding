from wedding.extensions.store.global_errors import ConstraintError
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.special_codes import GUESTS_CONSTRAINT_ERROR


class GuestsConstraintError(ConstraintError):
    def __init__(self, msg: str):
        super().__init__(
            model=Guests.__name__,
            msg=msg,
            special_code=GUESTS_CONSTRAINT_ERROR,
        )
