"""backend/plaid_client.py"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MockPlaidClient:
    """
    Mock Plaid client used for sandbox and early development.
    This stub simulates real Plaid API responses for testing.
    """

    def __init__(self):
        logger.info("Initialized Mock Plaid Client")

    def create_link_token(self, user_id: str) -> dict:
        """
        Simulate Plaid link token creation.
        """
        logger.debug(f"Creating mock link token for user {user_id}")
        return {
            "link_token": f"mock-link-token-{user_id}",
            "expiration": datetime.utcnow().isoformat(),
        }

    def exchange_public_token(self, public_token: str) -> dict:
        """
        Simulate exchanging a public token for an access token.
        """
        logger.debug(f"Exchanging mock public token: {public_token}")
        return {
            "access_token": f"mock-access-token-{public_token[-6:]}",
            "item_id": f"mock-item-{public_token[-6:]}",
        }

    def get_accounts(self, access_token: str) -> dict:
        """
        Return mock account data for the authenticated user.
        """
        logger.debug(f"Fetching mock accounts for access token: {access_token}")
        return {
            "accounts": [
                {
                    "account_id": "mock-checking-001",
                    "name": "Plaid Checking",
                    "type": "depository",
                    "subtype": "checking",
                    "balances": {"available": 1500.50, "current": 1500.50},
                },
                {
                    "account_id": "mock-savings-002",
                    "name": "Plaid Savings",
                    "type": "depository",
                    "subtype": "savings",
                    "balances": {"available": 3200.00, "current": 3200.00},
                },
            ]
        }

# Instantiate globally for easy import
plaid_client = MockPlaidClient()
