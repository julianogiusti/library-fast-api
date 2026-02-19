from http import HTTPStatus


class AppException(Exception):
    status_code: int = HTTPStatus.BAD_REQUEST
    title: str = "Application error"

    def __init__(self, message: str, *, status_code: int | None = None, title: str | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = int(status_code)
        if title is not None:
            self.title = title
        super().__init__(message)


class NotFoundException(AppException):
    status_code = HTTPStatus.NOT_FOUND
    title = "Not found"
