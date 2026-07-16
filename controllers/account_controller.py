from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from services.account_service import AccountService
from bson import ObjectId

account_bp = Blueprint("account", __name__, url_prefix="/api/accounts")


def build_account_blueprint(account_service: AccountService) -> Blueprint:

    @account_bp.route("/", methods=["POST"])
    @jwt_required()
    def create_account():
        user_id = get_jwt_identity()
        data = request.get_json()
        #user_id = data.get("userId")
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
        transaction, balance = account_service.deposit(id, amount)
        if transaction is None:
            return{"error": "amount must be greater than 0"}, 400
        return jsonify({"transaction": transaction.to_dict(), "balance": balance}), 201
    
    @account_bp.route("/<string:id>/withdraw", methods=["POST"])
    def withdraw(id):
        data = request.get_json()
        if data is None:
            return {"error": "no id provided"}, 400
        amount = data["amount"]
        if amount is None:
            return {"error": "no amount provided"}, 400
        transaction, balance = account_service.withdraw(id, amount)
        if transaction is None:
            return{"error": "amount must be greater than 0 and not greater than balance"}, 400
        return jsonify({"transaction": transaction.to_dict(), "balance": balance}), 201
    
    @account_bp.route("/<string:accountId>/transactions", methods=["GET"])
    def get_transactions(accountId):
        print(f"acc id for get transactions: {accountId}")
        transactions = account_service.get_transactions(accountId)
        if transactions is None:
            return {"error": "no transactions found"}, 404
        return jsonify([t.to_dict() for t in transactions]), 200
    
    @account_bp.route("/delete", methods=["DELETE"])
    @jwt_required()
    def delete_account():
        claims = get_jwt()
        data = request.get_json()
        if data is None:
            return {"error": "no accountId provided"}, 400
        accountId = data.get("accountId")
        isAdmin = claims.get("role") == "admin"
        if not isAdmin:
            return {"error": "admin privileges required"}, 403
        account = account_service.delete_account(accountId)
        if account is False:
            return {"error": "account not found"}, 404
        return {"message": "account deleted successfully"}, 200

    @account_bp.route("/admin/all", methods=["GET"])
    @jwt_required()
    def get_all_accounts_admin():
        claims = get_jwt()
        isAdmin = claims.get("role") == "admin"
        if not isAdmin:
            return {"error": "admin privileges required"}, 403
        accounts = account_service.get_all_accounts()
        return jsonify([account.to_dict() for account in accounts]), 200

    return account_bp
    
    
        


    
