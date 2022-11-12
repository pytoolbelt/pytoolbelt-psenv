from unittest.mock import MagicMock, patch
from psenv.core.config_file import ConfigFile
from psenv.environment.config import PSENV_YML


@patch("psenv.core.config_file.ConfigFile.parse_config")
def test_default_path(m_parse_config: MagicMock) -> None:
    m_parse_config.return_value = "test-value"
    config_file = ConfigFile()

    assert config_file.path == PSENV_YML
    assert config_file.config == "test-value"
    m_parse_config.assert_called_once()

