import pytest
from unittest.mock import patch, MagicMock
from argparse import Namespace
from pathlib import Path
from psenv.core.context import Context

@pytest.fixture
def mock_config():
    mock = MagicMock()
    mock.envfile = 'fake.env'
    return mock

@pytest.fixture
def mock_config_env():
    env = MagicMock()
    env.environment.account = '123456789012'
    env.environment.envfile = 'fake.env'
    env.parameter_path = '/fake/path'
    env.kms_key = 'fake-kms-key'
    return env

@patch('psenv.core.context.models.load_config')
@patch('psenv.core.context.aws.StsClient')
@patch('psenv.core.context.fileio.EnvFile')
@patch('psenv.core.context.aws.ParameterStoreClient')
@patch('psenv.core.context.load_dotenv')
def test_context_init(
    mock_load_dotenv,
    mock_ps_client,
    mock_env_file,
    mock_sts_client,
    mock_load_config,
    mock_config_env,
    mock_config
):
    # Setup mocks
    mock_load_config.return_value = mock_config
    mock_config.get_config_environment.return_value = mock_config_env
    mock_sts = MagicMock()
    mock_sts_client.return_value = mock_sts
    mock_env_file_instance = MagicMock()
    mock_env_file.return_value = mock_env_file_instance
    mock_ps_client_instance = MagicMock()
    mock_ps_client.return_value = mock_ps_client_instance

    ctx = Context(env='dev', config=Path('fake_config.yml'))

    mock_load_config.assert_called_once_with(Path('fake_config.yml'))
    mock_config.get_config_environment.assert_called_once_with('dev')
    mock_load_dotenv.assert_called_once_with('fake.env')
    mock_sts.raise_if_invalid_account.assert_called_once_with('123456789012')
    mock_env_file.assert_called_once_with(Path('fake.env'))
    mock_env_file_instance.load.assert_called_once()
    mock_ps_client.assert_called_once_with(parameter_path='/fake/path', kms_key='fake-kms-key')
    assert ctx.config == mock_config
    assert ctx.config_env == mock_config_env
    assert ctx.sts == mock_sts
    assert ctx.env_file == mock_env_file_instance
    assert ctx.ps_client == mock_ps_client_instance

@patch('psenv.core.context.Context.__init__', return_value=None)
def test_context_from_cliargs(mock_init):
    cliargs = Namespace(env='dev', config=Path('fake_config.yml'))
    Context.from_cliargs(cliargs)
    mock_init.assert_called_once_with(env='dev', config=Path('fake_config.yml'))

