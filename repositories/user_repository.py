from models import User
from bson import ObjectId
from mongoengine.errors import DoesNotExist

class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        try:
            return User.objects(email=email).first()
        except DoesNotExist:
            return None
    def find_by_id(self, user_id: str) -> User | None:
        try:
            return User.objects.get(id=ObjectId(user_id))
        except DoesNotExist:
            return None
    def register(self, email: str, name: str, role: str) -> User:
        user = User(email=email, name=name, role=role)
        user.save()
        return user
    def login(self, email: str, name: str) -> User | None:
        try:
            return User.objects(email=email, name=name).first()
        except DoesNotExist:
            return None