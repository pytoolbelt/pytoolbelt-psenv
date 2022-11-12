from pathlib import Path
from psenv.environment.config import PSENV_YML, PSENV_HOME


def test_psenv_home() -> None:
    expected_home = Path("~/.psenv").expanduser()
    assert expected_home == PSENV_HOME


def test_psenv_yml() -> None:
    expected_yml = Path("~/.psenv/psenv.yml").expanduser()
    assert expected_yml == PSENV_YML
