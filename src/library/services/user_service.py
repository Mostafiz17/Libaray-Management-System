from ..models.user import User

class UserService:

    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None