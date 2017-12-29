from app.models.error import Error
from app.constants.status_codes import HTTP_CODE_401_UNAUTHORIZED, HTTP_CODE_403_FORBIDDEN, HTTP_CODE_404_NOT_FOUND


class HTTPError (Error):

    @staticmethod
    def add_http_error_to(response, error):
        """Sets the response's status code to the error code then dds an error to the response."""
        if 100 <= error.code < 600:
            response.status_code = error.code
        Error.add_to_response_dict(response.response, error)

    @staticmethod
    def unauthorized():
        return Error(HTTP_CODE_401_UNAUTHORIZED,
                     "Unauthorized",
                     "Please sign in and try again.")

    @staticmethod
    def auth_invalid():
        return Error(HTTP_CODE_401_UNAUTHORIZED,
                     "Invalid username or password.",
                     "Please verify you have an account and check your username and password before trying again.")

    @staticmethod
    def auth_expired():
        return Error(HTTP_CODE_401_UNAUTHORIZED,
                     "Your sesdsion has expired.",
                     "Please sign in again.")

    @staticmethod
    def forbidden():
        return Error(HTTP_CODE_403_FORBIDDEN,
                     "Forbidden",
                     "You are not allowed to access this information.")

    @staticmethod
    def not_found(resource_name="resource"):
        return Error(HTTP_CODE_404_NOT_FOUND,
                     "Not Found",
                     "The " + resource_name + " you were looking for " +
                     "could not be found. Please adjust your query and try again.")
