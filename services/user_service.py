from flask_jwt_extended import create_access_token, create_refresh_token

from models import User
from repositories.user_repository import UserRepository




class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, email: str, name: str, role: str) -> User | None:
        
        if not email or not name:
            raise ValueError("Email and name are required")

        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        user = self.user_repository.register(email, name, role)
        return user

    def login(self, email: str, name: str) -> tuple[User, str, str]:
        if not email or not name:
            raise ValueError("Email and name are required")

        user = self.user_repository.login(email, name)

        if not user or user is None:
            raise ValueError("Invalid Credentials")
        if user.role == "admin":
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={
                    "role": user.role
                }
            )
        else:
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={
                    "role": "user"
                }
            )

        #access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return user, access_token, refresh_token
