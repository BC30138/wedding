from wedding.extensions.store.repo.groups.models import Groups
from wedding.extensions.store.repo.groups.special_codes import GROUPS_CONSTRAINT_ERROR
from wedding.extensions.store.global_errors import ConstraintError


class GroupsConstraintError(ConstraintError):
    def __init__(self, msg: str):
        super().__init__(
            model=Groups.__name__,
            msg=msg,
            special_code=GROUPS_CONSTRAINT_ERROR,
        )
