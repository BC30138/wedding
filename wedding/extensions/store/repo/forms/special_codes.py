"""Коды ошибок при выполнении выборки из бд бланков ответов."""

FORM_DB_ERROR = "FORM_DB_ERROR"  # неопознанная ошибка бд
FORM_CONSTRAINT_ERROR = "FORM_CONSTRAINT_ERROR"  # конфликт данных бланков ответов
FORM_MULTIPLE_ROWS_FOUND_ERROR = "FORM_MULTIPLE_ROWS_FOUND_ERROR"  # найдено несколько записей, когда должна одна
