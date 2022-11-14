from unittest.mock import MagicMock, patch
from psenv.core.config_file import ConfigFile
from psenv.environment.config import PSENV_YML


DUMMY_CONFIG = {"environments": {"foo": {"env": "some-env-value", "path": "some-path-value"}}}

EXPECTED_ENV = {"env": "some-env-value", "path": "some-path-value"}


@patch("psenv.core.config_file.ConfigFile.parse_config")
def test_default_path_and_constructor(m_parse_config: MagicMock) -> None:
    m_parse_config.return_value = "test-value"
    config_file = ConfigFile()

    assert config_file.path == PSENV_YML
    assert config_file.config == "test-value"
    m_parse_config.assert_called_once()


@patch("psenv.core.config_file.ConfigFile.parse_config")
def test_get_environment(m_parse_config: MagicMock) -> None:
    m_parse_config.return_value = DUMMY_CONFIG
    config_file = ConfigFile()

    env = config_file.get_environment("foo")
    assert env == EXPECTED_ENV


@patch("psenv.core.config_file.yaml")
@patch("psenv.core.config_file.ConfigFile.parse_config")
def test_save_config(m_parse_config: MagicMock, m_yaml: MagicMock) -> None:
    m_parse_config.return_value = DUMMY_CONFIG
    m_path = MagicMock()

    # mock the return value of the with statement
    m_stream = MagicMock()
    m_path.open.return_value.__enter__.return_value = m_stream

    config_file = ConfigFile(path=m_path)
    config_file.save_config()

    m_path.open.assert_called_once_with(mode="w+")
    m_yaml.dump.assert_called_once_with(data=DUMMY_CONFIG, stream=m_stream)
