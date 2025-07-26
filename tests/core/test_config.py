import os

import pytest

from psenv.core import config


@pytest.fixture
def reset_env_var():
    # Store original environment variable value
    original_value = os.environ.get("PSENV_RAISE_ERRORS")
    yield
    # Restore original environment variable state
    if original_value is not None:
        os.environ["PSENV_RAISE_ERRORS"] = original_value
    else:
        os.environ.pop("PSENV_RAISE_ERRORS", None)


def test_private_marker():
    assert config.PSENV_PRIVATE_MARKER == "#<private>"


def test_psenv_raise_errors_default(reset_env_var):
    if "PSENV_RAISE_ERRORS" in os.environ:
        del os.environ["PSENV_RAISE_ERRORS"]

    assert config.get_raise_errors_env() is False


def test_psenv_raise_errors_true(reset_env_var):
    os.environ["PSENV_RAISE_ERRORS"] = "true"
    assert config.get_raise_errors_env() is True


def test_psenv_raise_errors_false(reset_env_var):
    os.environ["PSENV_RAISE_ERRORS"] = "false"
    assert config.get_raise_errors_env() is False


def test_psenv_raise_errors_case_insensitive(reset_env_var):
    os.environ["PSENV_RAISE_ERRORS"] = "TRUE"
    assert config.get_raise_errors_env() is True


def test_psenv_raise_errors_invalid_value(reset_env_var):
    os.environ["PSENV_RAISE_ERRORS"] = "invalid"
    assert config.get_raise_errors_env() is False
