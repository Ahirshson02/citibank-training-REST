from decimal import Decimal, InvalidOperation
from models import Account, User, Transaction
from repositories.account_repository import AccountRepository
from repositories.user_repository import UserRepository

VALID_ACCOUNT_TYPES = {"checking", "savings"}



class AccountService:
    def __init__(self, account_repository: AccountRepository, user_repository: UserRepository):
        self.account_repository = account_repository
        self.user_repository = user_repository


    def create_account(self, user_id: str, account_type: str) -> Account:
        if account_type not in VALID_ACCOUNT_TYPES:
            return None
        user: User | None = self.user_repository.find_by_id(user_id)
        if user is None:
          #  print(f"User with id {user_id} not found.")
            return None
        return self.account_repository.create(user_id=user_id, account_type=account_type)

    def get_account(self, account_id: str) -> Account | None:
        return self.account_repository.find_by_id(account_id)

    def get_accounts_for_user(self, user_id: str) -> list[Account]:
        return self.account_repository.find_all_for_user(user_id)
    
    def get_all_accounts(self) -> list[Account]:
        return self.account_repository.find_all_accounts()

    def delete_account(self, account_id: str):
        account = self.account_repository.find_by_id(account_id)
        if account is None:
            return False
        self.account_repository.delete(account_id)
        return account

    def deposit(self, account_id: str, amount) -> Account:
        account = self.account_repository.find_by_id(account_id)
        if account is None:
            return None
        if amount <= 0:
            return None
        #run repo method to deposit into db and create and return a transaction object that is also stored in DB
        transaction, balance = self.account_repository.deposit(account_id, amount, "deposit")
        #account.balance = account.balance + amount
        return transaction, balance

    def withdraw(self, account_id: str, amount) -> Account:
        account = self.account_repository.find_by_id(account_id)
        if account is None:
            return None
        if account.balance < amount:
            return None
        transaction, balance = self.account_repository.withdraw(account_id, amount, "withdraw")
        #account.save()
        return transaction, balance
    
    def get_transactions(self, accountId: str) -> list[Transaction]:
        transactions = self.account_repository.get_transactions(accountId)
        if transactions is None:
            return None
        return transactions
