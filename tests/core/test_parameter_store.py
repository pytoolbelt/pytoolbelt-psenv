from unittest.mock import MagicMock, patch

import pytest

from psenv.core.parameter_store import ParameterStore

DUMMY_FETCH_RESPONSE = {"Parameters": [{"Name": "CAPITAN_AMERICA", "Value": "shield"}, {"Name": "the_hulk", "Value": "smash!"}]}

DUMMY_PUSH_RESPONSE = {"Version": "1984"}

DUMMY_PUSH_PARAMS = {"METALLICA": "Ride The Lightning"}

DUMMY_DELETE_PARAMS = {"SLAYER": "Seasons in the Abyss"}

DUMMY_PATH = "/metal/thrash"


@pytest.fixture(scope="module", autouse=True)
def mock_boto_client() -> MagicMock:
    with patch("psenv.core.parameter_store.boto3") as m_boto3:
        m_ssm_client = MagicMock()
        m_ssm_client.get_parameters_by_path.return_value = DUMMY_FETCH_RESPONSE
        m_ssm_client.put_parameter.return_value = DUMMY_PUSH_RESPONSE

        m_boto3.client.return_value = m_ssm_client

        yield m_boto3


def test_parameter_store_fetch(mock_boto_client: MagicMock) -> None:
    expected_params = {"CAPITAN_AMERICA": "shield", "THE_HULK": "smash!"}

    parameter_store = ParameterStore(DUMMY_PATH)
    params = parameter_store.fetch()

    assert params == expected_params


def test_parameter_store_push(mock_boto_client: MagicMock) -> None:
    expected_response = ["Posted /metal/thrash/METALLICA -- version 1984"]

    parameter_store = ParameterStore(DUMMY_PATH)
    response = parameter_store.push(DUMMY_PUSH_PARAMS)
    assert response == expected_response
