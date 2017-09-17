
ERRORS_KEY = "errors"


class Error:

    def __init__(self, code, title="", message=""):
        self.code = code
        self.title = title
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "title": self.title,
            "message": self.message
        }

    # Readability helper abstracting reusable method chaining
    @staticmethod
    def add_to(response, error):
        if ERRORS_KEY not in response:
            response[ERRORS_KEY] = []
        response[ERRORS_KEY].append(error.to_dict())

    # Central location for application generated errors
    @staticmethod
    def missing_required_param(param_name=None):
        error = Error(100,
                      "Missing Information",
                      "Please supply all required parameters.")
        if param_name:
            error.message += " ({})".format(param_name)

        return error

    @staticmethod
    def auth_invalid():
        return Error(101,
                     "Invalid username or password.",
                     "Please verify you have an account and check your username and password before trying again.")
