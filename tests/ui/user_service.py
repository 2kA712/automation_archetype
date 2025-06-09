import hashlib
from typing import Optional, Dict, List


class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.is_active = True
        self.roles = []

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self._hash_password(password) == self.password_hash

    def add_role(self, role: str):
        if role not in self.roles:
            self.roles.append(role)

    def has_role(self, role: str) -> bool:
        return role in self.roles


class UserService:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def create_user(self, username: str, email: str, password: str) -> User:
        if username in self.users:
            raise ValueError(f"Користувач {username} вже існує")

        if len(password) < 6:
            raise ValueError("Пароль має бути не менше 6 символів")

        user = User(username, email, password)
        self.users[username] = user
        return user

    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.get_user(username)
        if user and user.check_password(password) and user.is_active:
            return user
        return None

    def deactivate_user(self, username: str) -> bool:
        user = self.get_user(username)
        if user:
            user.is_active = False
            return True
        return False

    def get_all_users(self) -> List[User]:
        return list(self.users.values())

    def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False