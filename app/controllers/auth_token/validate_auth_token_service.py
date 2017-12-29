from flask import request


def is_authenticated():
    if "auth_token" in request.cookies:
        auth_token = request.cookies["auth_token"]
        print("auth_token: " + auth_token)
        payload, status = decode_auth_token(auth_token)
        print("payload: " + str(payload))


def auth_required(function):

    def wrapper():
        pass
    return wrapper


if __name__ == "__main__":
    auth_required()