"""finance/views.py"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.plaid_client import plaid_client

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_link_token(request):
    """
    Mock endpoint to return a Plaid link token.
    """
    token_data = plaid_client.create_link_token(request.user.id)
    return Response(token_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def exchange_public_token(request):
    """
    Mock endpoint to exchange public token for access token.
    """
    public_token = request.data.get("public_token")
    token_data = plaid_client.exchange_public_token(public_token)
    # Here you’d save the mock access_token + item_id to the user model
    return Response(token_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    """
    Mock endpoint to return account list.
    """
    mock_access_token = "mock-access-token-placeholder"
    accounts = plaid_client.get_accounts(mock_access_token)
    return Response(accounts)
