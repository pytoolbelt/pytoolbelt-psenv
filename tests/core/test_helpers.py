import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from psenv.core.helpers import parse_config


def override_psenv_yml() -> Path:
    return Path("foo-bar.bunk-file")


@patch("psenv.core.helpers.yaml")
@patch("psenv.core.helpers.PSENV_YML")
def test_parse_config(patched_psenv_yml: MagicMock, patched_yaml: MagicMock) -> None:
    mock_yml = MagicMock()
    patched_psenv_yml.open.return_value = mock_yml

    _ = parse_config()

    assert patched_yaml.safe_load.called_once_with(mock_yml)
    assert patched_yaml.open.called_once()


@patch("psenv.core.helpers.PSENV_YML", new_callable=override_psenv_yml)
def test_parse_config_raises_file_not_found(_) -> None:
    with pytest.raises(FileNotFoundError) as _:
        parse_config()
