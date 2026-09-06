from ..models.user import User
from ..storage.json_storage import JsonStorage


class UserService:

    def __init__(self):
        self.users = []
        self.storage = JsonStorage("data/users.json")

    def add_user(self, user):
        self.users.append(user)

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def save_users(self):

        data = []

        for user in self.users:
            data.append({
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email
            })

        self.storage.save(data)

        print("Users saved successfully.")

    def load_users(self):

        data = self.storage.load()

        self.users = []

        for user_data in data:

            user = User(
                user_data["user_id"],
                user_data["name"],
                user_data["email"]
            )

            self.users.append(user)

        print("Users loaded successfully.")