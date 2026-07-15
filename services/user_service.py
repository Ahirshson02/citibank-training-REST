from models import User
from repositories.user_repository import UserRepository




class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, email: str, name: str) -> User | None:
        
        if not email or not name:
            raise ValueError("Email and name are required")

        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        user = self.user_repository.register(email, name)
        return user

    def login(self, email: str, name: str) -> User:
        if not email or not name:
            raise ValueError("Email and name are required")

        user = self.user_repository.login(email, name)

        if not user or user is None:
            raise ValueError("Invalid Credentials")
        return user
