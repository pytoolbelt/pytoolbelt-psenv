import os

import pytest

from psenv.core.fileio import get_environment_variables, read_config, read_config_template
from psenv.error_handling.exceptions import PsenvConfigError, PsenvConfigNotFoundError, PsenvInternalError


def test_read_config_success(tmp_path):
    config_path = tmp_path / "psenv.yml"
    config_content = """
    envfile: .env
    root_path: /params
    environments:
      - name: dev
        account: "123456789012"
        envfile: .env.dev
    """
    config_path.write_text(config_content)

    result = read_config(config_path)

    assert isinstance(result, dict)
    assert result["envfile"] == ".env"
    assert result["root_path"] == "/params"
    assert len(result["environments"]) == 1


def test_read_config_with_env_vars(tmp_path):
    config_path = tmp_path / "psenv.yml"
    config_content = """
    envfile: ${ENV_FILE}
    root_path: /params
    """
    config_path.write_text(config_content)

    os.environ["ENV_FILE"] = ".env.test"
    result = read_config(config_path)

    assert result["envfile"] == ".env.test"
    del os.environ["ENV_FILE"]


def test_read_config_file_not_found(tmp_path):
    non_existent_path = tmp_path / "nonexistent.yml"

    with pytest.raises(PsenvConfigNotFoundError, match="psenv.yml not found in"):
        read_config(non_existent_path)


def test_read_config_invalid_yaml(tmp_path):
    config_path = tmp_path / "psenv.yml"
    invalid_content = """
    envfile: .env
    root_path: /params
    environments:
      - name: dev
        account: [invalid yaml
    """
    config_path.write_text(invalid_content)

    with pytest.raises(PsenvConfigError, match="Error loading psenv.yml"):
        read_config(config_path)


def test_read_config_template_success(tmp_path):
    template_path = tmp_path / "template.yml"
    template_content = """
    envfile: .env
    root_path: /params
    environments: []
    """
    template_path.write_text(template_content)

    result = read_config_template(template_path)
    assert result == template_content


def test_read_config_template_file_not_found(tmp_path):
    non_existent_path = tmp_path / "nonexistent.yml"

    with pytest.raises(PsenvInternalError, match="psenv template file not found at"):
        read_config_template(non_existent_path)


def test_read_config_template_default_path():
    with pytest.raises(PsenvInternalError) as exc_info:
        read_config_template()
    assert "psenv template file not found at" in str(exc_info.value)
    assert "Please file a bug report" in str(exc_info.value)


@pytest.fixture
def mock_env_vars():
    # Setup test environment variables
    original_env = os.environ.copy()
    os.environ.update({"APP_NAME": "myapp", "APP_VERSION": "1.0.0", "APP_PORT": "8080", "OTHER_VAR": "test", "SYSTEM_PATH": "/usr/local"})
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_get_environment_variables_with_prefix(mock_env_vars):
    result = get_environment_variables("APP")

    assert len(result) == 3
    assert result["APP_NAME"] == "myapp"
    assert result["APP_VERSION"] == "1.0.0"
    assert result["APP_PORT"] == "8080"


def test_get_environment_variables_no_matches(mock_env_vars):
    result = get_environment_variables("NONEXISTENT")

    assert isinstance(result, dict)
    assert len(result) == 0


def test_get_environment_variables_case_sensitive(mock_env_vars):
    result = get_environment_variables("app")
    assert len(result) == 3


def test_get_environment_variables_empty_prefix(mock_env_vars):
    result = get_environment_variables("")
    assert isinstance(result, dict)
    assert len(result) == len(os.environ)
