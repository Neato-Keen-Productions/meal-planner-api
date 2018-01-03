from app.constants import MAX_USERNAME_LEGNTH, MAX_PASSWORD_LENGTH, MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, ERRORS_KEY, MIN_INGREDIENT_NAME_LENGTH, MAX_INGREDIENT_NAME_LENGTH


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

    @staticmethod
    def password_too_long():
        return Error(903,
                     "Password too long.",
                     "Please make sure that password is less than " + str(MAX_PASSWORD_LENGTH) +" characters long.")

    @staticmethod
    def password_too_short():
        return Error(902,
                     "Password is too short.",
                     "Please enter a password that is at least "+ str(MIN_PASSWORD_LENGTH) + " characters long.")

    @staticmethod
    def username_is_taken():
        return Error(900,
                     "Username is taken.",
                     "Please choose another username.")

    @staticmethod
    def username_contains_spaces():
        return Error(904,
                     "Username is contains spaces.",
                     "Please remove spaces from username and try again.")

    @staticmethod
    def username_too_long():
        return Error(905,
                     "Username too long.",
                     "Please enter a username less than " + str(MAX_USERNAME_LEGNTH) + " in length.")

    @staticmethod
    def username_too_short():
        return Error(901,
                     "Username is too short.",
                     "Please enter a username more than " + str(MIN_USERNAME_LENGTH) + " in length.")

    @staticmethod
    def ingredient_name_too_short():
        return Error(801,
                     "Ingredient name is too short.",
                     "Please enter an ingredient name more than " + str(MIN_INGREDIENT_NAME_LENGTH) + " in length.")

    @staticmethod
    def ingredient_name_too_long():
        return Error(802,
                     "Ingredient name is too long.",
                     "Please enter an ingredient name less than " + str(MAX_INGREDIENT_NAME_LENGTH) + " in length.")

    @staticmethod
    def ingredient_name_taken():
        return Error(800,
                     "Ingredient name is taken.",
                     "Please enter a different name for your ingredient. Creating a new ingredient may not be required.")
