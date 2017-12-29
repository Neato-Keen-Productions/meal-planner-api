from flask import g
from functools import wraps
from app.models.http_error import HTTPError
from app.constants.status_codes import *


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "errors" in g.response.response:
            for error in g.response.response["errors"]:
                if error["code"] is HTTP_CODE_403_FORBIDDEN:
                    g.response.status_code = HTTP_CODE_403_FORBIDDEN
                else:
                    g.response.status_code = HTTP_CODE_401_UNAUTHORIZED
            return g.response
        elif g.user:
            return f(*args, **kwargs)
        else:
            error = HTTPError.unauthorized()
            HTTPError.add_http_error_to(g.response, error)
            return g.response

    return decorated_function

