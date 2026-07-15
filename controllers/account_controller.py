from flask import Blueprint, request, jsonify
from services.account_service import AccountService
from bson import ObjectId

account_bp = Blueprint("account", __name__, url_prefix="/api/accounts")


def build_account_blueprint(account_service: AccountService) -> Blueprint:

    @account_bp.route("/", methods=["POST"])
    def create_account():
        print("create_account called")
        data = request.get_json()
        user_id = data.get("userId")
        account_type = data.get("accountType")
        
        account = account_service.create_account(user_id, account_type)
        
        return jsonify(account.to_dict()), 201
    
    @account_bp.route("/<string:id>", methods=["GET"])
    def get_account(id):
        
        account = account_service.get_account(id)
        if account is None:
            return {"error": "account not found"}, 404
        return jsonify(account.to_dict()), 200
    
    @account_bp.route("/<string:userId>/all", methods=["GET"])
    def get_all_accounts(userId):
        accounts = account_service.get_accounts_for_user(userId)
        if accounts is None:
            return {"error": "accounts not found"}, 404
        return jsonify([account.to_dict() for account in accounts]), 200


    @account_bp.route("/<string:id>/deposit", methods=["POST"])
    def deposit(id):
        data = request.get_json()
        if data is None:
            return {"error": "no id provided"}, 400
        amount = data["amount"]
        if amount is None:
            return {"error": "no amount provided"}, 400
        transaction = account_service.deposit(id, amount)
        if transaction is None:
            return{"error": "amount must be greater than 0"}, 400
        return jsonify(transaction.to_dict()), 201
    
    @account_bp.route("/<string:id>/withdraw", methods=["POST"])
    def withdraw(id):
        data = request.get_json()
        if data is None:
            return {"error": "no id provided"}, 400
        amount = data["amount"]
        if amount is None:
            return {"error": "no amount provided"}, 400
        transaction = account_service.withdraw(id, amount)
        if transaction is None:
            return{"error": "amount must be greater than 0 and not greater than balance"}, 400
        return jsonify(transaction.to_dict()), 201
    
    @account_bp.route("/<string:userId>/transactions", methods=["GET"])
    def get_transactions(userId):
        transactions = account_service.get_transactions(userId)
        if transactions is None:
            return {"error": "no transactions found"}, 404
        return jsonify([t.to_dict() for t in transactions]), 200
    
    return account_bp
    
    
        


    
