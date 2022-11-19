from pathlib import Path
from psenv.environment.config import (
    PSENV_YML,
    PSENV_HOME,
    PSENV_ENV_FILE,
    PSENV_TEMPLATE_PREFIX,
    PSENV_PRIVATE_MARKER
)


def test_psenv_home() -> None:
    expected_home = Path("~/.psenv").expanduser()
    assert expected_home == PSENV_HOME


def test_psenv_yml() -> None:
    expected_yml = Path("~/.psenv/psenv.yml").expanduser()
    assert expected_yml == PSENV_YML


def test_psenv_env() -> None:
    expected_env = Path("~/.psenv/psenv.env").expanduser()
    assert expected_env == PSENV_ENV_FILE


def test_psenv_template_prefix() -> None:
    assert PSENV_TEMPLATE_PREFIX == "PSENV__TEMPLATE__"


def test_psenv_private_marker() -> None:
    assert PSENV_PRIVATE_MARKER == "#<private>"
