"""
Pytest tests for the account Flask blueprint routes.

These tests focus purely on the controller/route layer:
- request parsing
- status codes
- response bodies
- how the routes react to different return values from AccountService

AccountService itself is mocked out (MagicMock), so none of its internal
logic is exercised here -- only the contract between the routes and the
service (i.e. what the routes do with whatever the service returns).

Adjust the import below to match wherever `build_account_blueprint` actually
lives in your project, e.g.:

    from routes.account_routes import build_account_blueprint
"""

import pytest
from unittest.mock import MagicMock
from flask import Flask

from controllers.account_controller import build_account_blueprint 


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mock_account_service():
    return MagicMock()


@pytest.fixture(scope="module")
def app(mock_account_service):
    app = Flask(__name__)
    blueprint = build_account_blueprint(mock_account_service)
    app.register_blueprint(blueprint)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_mock(mock_account_service):
    """Ensure each test starts with a clean mock (no leftover call history
    or return values from a previous test)."""
    mock_account_service.reset_mock(return_value=True, side_effect=True)
    yield


def make_fake_model(data):
    """Helper to build a stand-in for Account/Transaction model objects
    that only need a to_dict() method for these routes."""
    model = MagicMock()
    model.to_dict.return_value = data
    return model


# ---------------------------------------------------------------------------
# POST /api/accounts/  (create_account)
# ---------------------------------------------------------------------------

class TestCreateAccount:
    def test_create_account_success(self, client, mock_account_service):
        expected = {"id": "acc123", "userId": "user1", "accountType": "checking"}
        mock_account_service.create_account.return_value = make_fake_model(expected)

        response = client.post(
            "/api/accounts/",
            json={"userId": "user1", "accountType": "checking"},
        )

        assert response.status_code == 201
        assert response.get_json() == expected
        mock_account_service.create_account.assert_called_once_with("user1", "checking")

    def test_create_account_missing_fields_passes_none_to_service(
        self, client, mock_account_service
    ):
        expected = {"id": "acc123", "userId": None, "accountType": None}
        mock_account_service.create_account.return_value = make_fake_model(expected)

        response = client.post("/api/accounts/", json={})

        assert response.status_code == 201
        mock_account_service.create_account.assert_called_once_with(None, None)


# ---------------------------------------------------------------------------
# GET /api/accounts/<id>  (get_account)
# ---------------------------------------------------------------------------

class TestGetAccount:
    def test_get_account_found(self, client, mock_account_service):
        expected = {"id": "acc123", "userId": "user1", "accountType": "checking"}
        mock_account_service.get_account.return_value = make_fake_model(expected)

        response = client.get("/api/accounts/acc123")

        assert response.status_code == 200
        assert response.get_json() == expected
        mock_account_service.get_account.assert_called_once_with("acc123")

    def test_get_account_not_found(self, client, mock_account_service):
        mock_account_service.get_account.return_value = None

        response = client.get("/api/accounts/doesnotexist")

        assert response.status_code == 404
        assert response.get_json() == {"error": "account not found"}


# ---------------------------------------------------------------------------
# GET /api/accounts/<userId>/all  (get_all_accounts)
# ---------------------------------------------------------------------------

class TestGetAllAccounts:
    def test_get_all_accounts_found(self, client, mock_account_service):
        acc1 = make_fake_model({"id": "acc1"})
        acc2 = make_fake_model({"id": "acc2"})
        mock_account_service.get_accounts_for_user.return_value = [acc1, acc2]

        response = client.get("/api/accounts/user1/all")

        assert response.status_code == 200
        assert response.get_json() == [{"id": "acc1"}, {"id": "acc2"}]
        mock_account_service.get_accounts_for_user.assert_called_once_with("user1")

    def test_get_all_accounts_empty_list_returns_empty_array(
        self, client, mock_account_service
    ):
        mock_account_service.get_accounts_for_user.return_value = []

        response = client.get("/api/accounts/user1/all")

        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_all_accounts_none_returns_404(self, client, mock_account_service):
        mock_account_service.get_accounts_for_user.return_value = None

        response = client.get("/api/accounts/user1/all")

        assert response.status_code == 404
        assert response.get_json() == {"error": "accounts not found"}


# ---------------------------------------------------------------------------
# POST /api/accounts/<id>/deposit  (deposit)
# ---------------------------------------------------------------------------

class TestDeposit:
    def test_deposit_success(self, client, mock_account_service):
        expected = {"id": "txn1", "amount": 100, "type": "deposit"}
        mock_account_service.deposit.return_value = make_fake_model(expected)

        response = client.post("/api/accounts/acc123/deposit", json={"amount": 100})

        assert response.status_code == 201
        assert response.get_json() == expected
        mock_account_service.deposit.assert_called_once_with("acc123", 100)

    def test_deposit_no_json_body_returns_400(self, client, mock_account_service):
        # request.get_json() only returns None (rather than raising) when the
        # body parses to the JSON literal `null`, so that's what triggers the
        # "if data is None" branch in the route.
        response = client.post(
            "/api/accounts/acc123/deposit",
            data="null",
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.get_json() == {"error": "no id provided"}
        mock_account_service.deposit.assert_not_called()

    def test_deposit_amount_none_returns_400(self, client, mock_account_service):
        response = client.post("/api/accounts/acc123/deposit", json={"amount": None})

        assert response.status_code == 400
        assert response.get_json() == {"error": "no amount provided"}
        mock_account_service.deposit.assert_not_called()

    def test_deposit_invalid_amount_service_returns_none(
        self, client, mock_account_service
    ):
        mock_account_service.deposit.return_value = None

        response = client.post("/api/accounts/acc123/deposit", json={"amount": -5})

        assert response.status_code == 400
        assert response.get_json() == {"error": "amount must be greater than 0"}


# ---------------------------------------------------------------------------
# POST /api/accounts/<id>/withdraw  (withdraw)
# ---------------------------------------------------------------------------

class TestWithdraw:
    def test_withdraw_success(self, client, mock_account_service):
        expected = {"id": "txn2", "amount": 50, "type": "withdraw"}
        mock_account_service.withdraw.return_value = make_fake_model(expected)

        response = client.post("/api/accounts/acc123/withdraw", json={"amount": 50})

        assert response.status_code == 201
        assert response.get_json() == expected
        mock_account_service.withdraw.assert_called_once_with("acc123", 50)

    def test_withdraw_no_json_body_returns_400(self, client, mock_account_service):
        # Same reasoning as the deposit equivalent: get_json() returns None
        # (instead of raising) only for a literal JSON `null` body.
        response = client.post(
            "/api/accounts/acc123/withdraw",
            data="null",
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.get_json() == {"error": "no id provided"}
        mock_account_service.withdraw.assert_not_called()

    def test_withdraw_amount_none_returns_400(self, client, mock_account_service):
        response = client.post("/api/accounts/acc123/withdraw", json={"amount": None})

        assert response.status_code == 400
        assert response.get_json() == {"error": "no amount provided"}
        mock_account_service.withdraw.assert_not_called()

    def test_withdraw_invalid_amount_service_returns_none(
        self, client, mock_account_service
    ):
        mock_account_service.withdraw.return_value = None

        response = client.post("/api/accounts/acc123/withdraw", json={"amount": 999999})

        assert response.status_code == 400
        assert response.get_json() == {
            "error": "amount must be greater than 0 and not greater than balance"
        }


# ---------------------------------------------------------------------------
# GET /api/accounts/<userId>/transactions  (get_transactions)
# ---------------------------------------------------------------------------

class TestGetTransactions:
    def test_get_transactions_found(self, client, mock_account_service):
        t1 = make_fake_model({"id": "txn1", "amount": 10})
        t2 = make_fake_model({"id": "txn2", "amount": 20})
        mock_account_service.get_transactions.return_value = [t1, t2]

        response = client.get("/api/accounts/user1/transactions")

        assert response.status_code == 200
        assert response.get_json() == [
            {"id": "txn1", "amount": 10},
            {"id": "txn2", "amount": 20},
        ]
        mock_account_service.get_transactions.assert_called_once_with("user1")

    def test_get_transactions_none_returns_404(self, client, mock_account_service):
        mock_account_service.get_transactions.return_value = None

        response = client.get("/api/accounts/user1/transactions")

        assert response.status_code == 404
        assert response.get_json() == {"error": "no transactions found"}