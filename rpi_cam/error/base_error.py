class BaseResponse(Exception):
    def __init__(self, base_error, status_code, payload=None):
        Exception.__init__(self)
        self.base_error = base_error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.base_error.message
        return rv


class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class ValidationError(BaseError):
    def __init__(self, form):
        self.message = form.errors
