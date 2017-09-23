from app.models.user import User

def get_user_from_username(username):
    return User.query.filter_by(username=username).first()
