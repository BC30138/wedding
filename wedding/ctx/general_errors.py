DEFAULT_SPECIAL_CODE = "UNEXPECTED_DOMAIN_ERROR"


class DomainError(Exception):
    special_code = DEFAULT_SPECIAL_CODE

    def __init__(self, entity: str, msg: str, special_code: str | None = None):
        self.entity = entity
        self.msg = msg
        self.special_code = special_code
        super().__init__(self.msg)


class EntityValidationError(DomainError):
    pass
