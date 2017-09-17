from app.models.user import User


class UserDAO:

    @staticmethod
    def get_user_from_username(username):
        return User.query.filter_by(username=username).first()
