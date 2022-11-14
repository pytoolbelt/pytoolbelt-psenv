import os
from unittest.mock import patch
from psenv.core.helpers import get_environment_variables

DUMMY_ENVIRON = {"FOO_VAR1": "spam", "FOO_VAR2": "beans", "FOO_VAR3": "eggs"}


@patch.dict(os.environ, DUMMY_ENVIRON, clear=True)
def test_get_environment_variables() -> None:
    params = get_environment_variables("FOO")
    assert params == DUMMY_ENVIRON


@patch.dict(os.environ, DUMMY_ENVIRON, clear=True)
def test_get_environment_variables_lower() -> None:
    params = get_environment_variables("foo")
    assert params == DUMMY_ENVIRON
