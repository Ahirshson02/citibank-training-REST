from decimal import Decimal
from datetime import datetime
import mongoengine as me


class User(me.Document):
    meta = {
        "collection": "users",
    }

    name = me.StringField(max_length=100)
    email = me.EmailField(required=True, unique=True, max_length=100)
    created_at = me.DateTimeField(default=datetime.now())
    role = me.StringField(max_length=20, default="user")  
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Account(me.Document):
    meta = {
        "collection": "accounts",
        "indexes": [
            "user",
        ],
    }

    user = me.ReferenceField(
        User,
        required=True,
        reverse_delete_rule=me.CASCADE,
    )


    balance = me.DecimalField(
        precision=2,
        default=Decimal("0.00"),
        min_value=Decimal("0.00"),
    )

    account_type = me.StringField(max_length=50)
    created_at = me.DateTimeField(default=datetime.now())

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user.id),
            "balance": str(self.balance),
            "account_type": self.account_type,
            "created_at": self.created_at.isoformat(),
        }

class Transaction(me.Document):
    meta = {
        "collection": "transactions",
        "indexes": [
            "account",
        ],
    }

    account = me.ReferenceField(
        Account,
        required=True,
        reverse_delete_rule=me.CASCADE,
    )

    txn_type = me.StringField(max_length=20)

    amount = me.DecimalField(
        required=True,
        precision=2,
    )
    created_at = me.DateTimeField(default=datetime.now())

    def to_dict(self):
        return {
            "id": str(self.id),
            "account_id": str(self.account.id),
            "txn_type": self.txn_type,
            "amount": str(self.amount),
            "created_at": self.created_at.isoformat(),
        }

