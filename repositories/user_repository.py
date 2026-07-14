from models import User
from bson import ObjectId
from mongoengine.errors import DoesNotExist

class UserRepository:
    def find_by_id(self, user_id: str) -> User | None:
        try:
            return User.objects.get(id=ObjectId(user_id))
        except DoesNotExist:
            return None