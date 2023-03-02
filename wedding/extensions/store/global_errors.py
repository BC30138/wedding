DEFAULT_SPECIAL_CODE = "UNEXPECTED_STORE_ERROR"


class StoreError(Exception):
    special_code = DEFAULT_SPECIAL_CODE

    def __init__(self, model: str, msg: str, special_code: str | None = None):
        self.model = model
        self.msg = msg
        if special_code is not None:
            self.special_code = special_code
        super().__init__(self.msg)
