from pathlib import Path

import pytest

from psenv.core.config import PSENV_PRIVATE_MARKER
from psenv.core.fileio import EnvFile


@pytest.fixture
def env_file(tmp_path) -> EnvFile:
    return EnvFile(tmp_path / ".env")


@pytest.fixture
def sample_env_content():
    return """
# ----------------------------APP------------------------------------ #
APP_NAME='testapp'
APP_VERSION='1.0.0'

# ----------------------------DB------------------------------------ #
DB_HOST='localhost'
DB_PORT='5432'

#<private>

# ----------------------------SECRET------------------------------------ #
SECRET_KEY='mysecret'
SECRET_TOKEN='mytoken'
"""


def test_env_file_initialization(tmp_path):
    path = tmp_path / ".env"
    env_file = EnvFile(path)

    assert env_file.path == path.absolute()
    assert path.exists()
    assert isinstance(env_file.local_params, dict)
    assert len(env_file.local_params) == 0


def test_env_file_load(env_file, sample_env_content):
    env_file.path.write_text(sample_env_content)
    env_file.load()

    assert len(env_file.local_params) == 4
    assert env_file.local_params["APP_NAME"] == "testapp"
    assert env_file.local_params["DB_HOST"] == "localhost"

    private_params = env_file.get_params("private")
    assert len(private_params) == 2
    assert private_params["SECRET_KEY"] == "mysecret"


def test_env_file_update_params(env_file):
    new_params = {"APP_NAME": "newapp", "APP_PORT": "8080"}
    env_file.update_params(new_params, "main")

    assert env_file.local_params["APP_NAME"] == "newapp"
    assert env_file.local_params["APP_PORT"] == "8080"


def test_env_file_write_params(env_file):
    main_params = {"APP_NAME": "testapp", "DB_HOST": "localhost"}
    private_params = {"SECRET_KEY": "mysecret"}

    env_file.update_params(main_params, "main")
    env_file.update_params(private_params, "private")
    env_file.write_params()

    content = env_file.path.read_text()
    assert "APP_NAME='testapp'" in content
    assert "DB_HOST='localhost'" in content
    assert PSENV_PRIVATE_MARKER in content
    assert "SECRET_KEY='mysecret'" in content


def test_env_file_get_nonexistent_section(env_file):
    params = env_file.get_params("nonexistent")
    assert isinstance(params, dict)
    assert len(params) == 0


def test_env_file_empty_content(env_file):
    env_file.path.write_text("")
    env_file.load()

    assert len(env_file.local_params) == 0
    assert len(env_file.get_params("private")) == 0


def test_env_file_with_expanduser(tmp_path):
    env_file = EnvFile(Path("~/test/.env"))

    assert "~" not in str(env_file.path)
    assert env_file.path.is_absolute()
