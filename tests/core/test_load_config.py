from pathlib import Path
from unittest.mock import patch

import pytest

from psenv.core.models import PsenvConfig, PsenvConfigError, load_config


@pytest.fixture
def valid_config_dict():
    return {"envfile": ".env", "root_path": "/params", "environments": [{"name": "dev", "account": "123456789012", "envfile": ".env.dev"}]}


def test_load_config_with_valid_path(tmp_path, valid_config_dict):
    config_path = tmp_path / "psenv.yaml"
    with patch("psenv.core.models.read_config") as mock_read_config:
        mock_read_config.return_value = valid_config_dict

        config = load_config(config_path)

        assert isinstance(config, PsenvConfig)
        assert config.envfile == ".env"
        assert config.root_path == "/params"
        mock_read_config.assert_called_once_with(config_path)


def test_load_config_without_path(valid_config_dict):
    with (
        patch("psenv.core.models.read_config") as mock_read_config,
        patch("psenv.core.models.PSENV_CONFIG_FILE_PATH", Path("/default/path")),
    ):
        mock_read_config.return_value = valid_config_dict

        config = load_config()

        assert isinstance(config, PsenvConfig)
        mock_read_config.assert_called_once_with(Path("/default/path"))


def test_load_config_with_invalid_config():
    invalid_config = {
        "envfile": ".env",
        "root_path": "invalid_path",  # missing leading slash
        "environments": [],
    }

    with patch("psenv.core.models.read_config") as mock_read_config:
        mock_read_config.return_value = invalid_config

        with pytest.raises(PsenvConfigError, match="Error loading config"):
            load_config()


def test_load_config_with_missing_required_fields():
    incomplete_config = {
        "root_path": "/params"  # missing required fields
    }

    with patch("psenv.core.models.read_config") as mock_read_config:
        mock_read_config.return_value = incomplete_config

        with pytest.raises(PsenvConfigError, match="Error loading config"):
            load_config()
