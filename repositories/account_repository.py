
from models import Account, Transaction
from bson import ObjectId
from mongoengine.errors import DoesNotExist, defaultdict
from decimal import Decimal


class AccountRepository:
    def find_by_id(self, account_id):
        try:
            return Account.objects.get(id=ObjectId(account_id))
        except DoesNotExist:
            return None

    def find_all_for_user(self, user_id: str) -> list[Account]:
        return Account.objects.filter(user=user_id).all()
  
    def find_all_accounts(self) -> list[Account]:
        return list(
            Account.objects.order_by("user")
        )
    def create(self, user_id: str, account_type):
        return Account.objects.create(user=user_id, account_type=account_type, balance=0)
    def delete(self, account_id: str):
        account = self.find_by_id(account_id)
        if account:
            account.delete()
            account.save()
            return True
        return False
    def deposit(self, account_id, amount, type):
        account = Account.objects.get(id=ObjectId(account_id))
        account.balance = account.balance + Decimal(amount)
        transaction = Transaction.objects.create(account=account_id, txn_type=type, amount=amount)
        account.save()
        return transaction, account.balance
    def withdraw(self, account_id, amount, type):
        account = Account.objects.get(id=ObjectId(account_id))
        account.balance = account.balance - Decimal(amount)
        transaction = Transaction.objects.create(account=account_id, txn_type=type, amount=amount)
        account.save()
        return transaction, account.balance
    def get_transactions(self, account_id: str) -> list[Transaction]:
        return Transaction.objects.filter(account=account_id).all()