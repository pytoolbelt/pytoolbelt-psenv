from unittest.mock import MagicMock

import pytest

from psenv.aws.parameter_store import ParameterStoreClient
from psenv.error_handling.exceptions import PsenvParameterStoreError


@pytest.fixture
def mock_ssm():
    return MagicMock()


def test_init_sets_properties(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm, kms_key="my-key")
    assert client.parameter_path == "/foo/bar"
    assert client.ssm == mock_ssm
    assert client.kms_key == "my-key"


def test_kms_key_default(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    assert client.kms_key == "alias/aws/ssm"


def test_get_params_kwargs(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    kwargs = client.get_params_kwargs
    assert kwargs["Path"] == "/foo/bar"
    assert kwargs["Recursive"] is True
    assert kwargs["WithDecryption"] is True


def test_put_params_kwargs(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm, kms_key="my-key")
    kwargs = client.put_params_kwargs("FOO", "bar", True)
    assert kwargs["Name"] == "/foo/bar/FOO"
    assert kwargs["Value"] == "bar"
    assert kwargs["Type"] == "SecureString"
    assert kwargs["Overwrite"] is True
    assert kwargs["KeyId"] == "my-key"


def test_parse_parameter_name():
    assert ParameterStoreClient.parse_parameter_name("/foo/bar/BAZ") == "BAZ"
    assert ParameterStoreClient.parse_parameter_name("BAZ") == "BAZ"


def test_get_parameters_success(mock_ssm):
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"Parameters": [{"Name": "/foo/bar/FOO", "Value": "bar"}]},
        {"Parameters": [{"Name": "/foo/bar/BAZ", "Value": "qux"}]},
    ]
    mock_ssm.get_paginator.return_value = paginator
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    params = client.get_parameters()
    assert params == {"FOO": "bar", "BAZ": "qux"}


def test_get_parameters_error(mock_ssm):
    paginator = MagicMock()
    paginator.paginate.side_effect = Exception("fail")
    mock_ssm.get_paginator.return_value = paginator
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    with pytest.raises(PsenvParameterStoreError):
        client.get_parameters()


def test_put_parameters_success(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm, kms_key="k")
    params = {"FOO": "bar"}
    client.put_parameters(params, overwrite=True)
    mock_ssm.put_parameter.assert_called_once()
    call_args = mock_ssm.put_parameter.call_args[1]
    assert call_args["Name"] == "/foo/bar/FOO"
    assert call_args["Value"] == "bar"
    assert call_args["Overwrite"] is True
    assert call_args["KeyId"] == "k"


def test_put_parameters_error(mock_ssm):
    mock_ssm.put_parameter.side_effect = Exception("fail")
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    with pytest.raises(PsenvParameterStoreError):
        client.put_parameters({"FOO": "bar"})


def test_delete_parameters_success(mock_ssm):
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    client.delete_parameters({"FOO": "bar"})
    mock_ssm.delete_parameter.assert_called_once_with(Name="/foo/bar/FOO")


def test_delete_parameters_error(mock_ssm):
    mock_ssm.delete_parameter.side_effect = Exception("fail")
    client = ParameterStoreClient("/foo/bar", ssm_client=mock_ssm)
    with pytest.raises(PsenvParameterStoreError):
        client.delete_parameters({"FOO": "bar"})
