from unittest.mock import MagicMock

import pytest

from psenv.aws.sts import StsClient
from psenv.error_handling.exceptions import PsenvInternalError, PsenvInvalidAccountError


@pytest.fixture
def mock_sts_client():
    mock = MagicMock()
    mock.get_caller_identity.return_value = {"Account": "123456789012", "UserId": "AID...", "Arn": "arn:aws:iam::123456789012:user/test"}
    return mock


def test_stsclient_init_uses_passed_client(mock_sts_client):
    client = StsClient(sts_client=mock_sts_client)
    assert client.sts == mock_sts_client


def test_stsclient_init_creates_client(monkeypatch):
    mock_boto = MagicMock()
    monkeypatch.setattr("boto3.client", lambda service: mock_boto if service == "sts" else None)
    client = StsClient()
    assert client.sts == mock_boto


def test_caller_identity_property_caches(mock_sts_client):
    client = StsClient(sts_client=mock_sts_client)
    # First access triggers get_caller_identity
    identity1 = client.caller_identity
    # Second access uses cached value
    identity2 = client.caller_identity
    assert identity1 == identity2
    mock_sts_client.get_caller_identity.assert_called_once()


def test_account_id_property(mock_sts_client):
    client = StsClient(sts_client=mock_sts_client)
    assert client.account_id == "123456789012"


def test_get_caller_identity_success(mock_sts_client):
    client = StsClient(sts_client=mock_sts_client)
    result = client.get_caller_identity()
    assert result["Account"] == "123456789012"
    mock_sts_client.get_caller_identity.assert_called_once()


def test_get_caller_identity_error():
    mock = MagicMock()
    mock.get_caller_identity.side_effect = Exception("fail")
    client = StsClient(sts_client=mock)
    with pytest.raises(PsenvInternalError) as excinfo:
        client.get_caller_identity()
    assert "Failed to get caller identity" in str(excinfo.value)


def test_raise_if_invalid_account_valid(mock_sts_client):
    client = StsClient(sts_client=mock_sts_client)
    # Should not raise
    client.raise_if_invalid_account("123456789012")


def test_raise_if_invalid_account_invalid(mock_sts_client):
    mock_sts_client.get_caller_identity.return_value = {"Account": "999999999999"}
    client = StsClient(sts_client=mock_sts_client)
    with pytest.raises(PsenvInvalidAccountError) as excinfo:
        client.raise_if_invalid_account("123456789012")
    assert "Invalid AWS account ID" in str(excinfo.value)
