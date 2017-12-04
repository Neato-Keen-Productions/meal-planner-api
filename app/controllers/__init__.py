from flask import g

from app.models.error import Error


def get_required_key_from_params(key, params):
    value = None
    if key in params:
        value = params[key]
    else:
        Error.add_to(g.response.response, Error.missing_required_param(key))

    return value
