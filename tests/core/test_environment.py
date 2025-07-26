import pytest
from psenv.core.models import Environment
from psenv.error_handling.exceptions import PsenvConfigError


def test_valid_environment_creation():
    env = Environment(
        name="dev",
        account="123456789012",
        envfile=".env",
        kms_key="alias/mykey",
        path="/params/dev"
    )
    assert env.name == "dev"
    assert env.account == "123456789012"
    assert env.envfile == ".env"
    assert env.kms_key == "alias/mykey"
    assert env.path == "/params/dev"


def test_minimal_environment_creation():
    env = Environment(
        name="dev",
        account="123456789012",
        envfile=".env"
    )
    assert env.name == "dev"
    assert env.account == "123456789012"
    assert env.envfile == ".env"
    assert env.kms_key is None
    assert env.path is None


def test_invalid_account():
    with pytest.raises(PsenvConfigError, match="AWS account ID must be a 12-digit numeric string"):
        Environment(
            name="dev",
            account="123",  # too short
            envfile=".env"
        )

    with pytest.raises(PsenvConfigError, match="AWS account ID must be a 12-digit numeric string"):
        Environment(
            name="dev",
            account="12345678901a",  # contains letter
            envfile=".env"
        )


def test_invalid_path():
    with pytest.raises(PsenvConfigError, match="Path must start with '/'"):
        Environment(
            name="dev",
            account="123456789012",
            envfile=".env",
            path="invalid/path"
        )


def test_invalid_kms_key():
    with pytest.raises(PsenvConfigError, match="KMS key must start with 'alias/'"):
        Environment(
            name="dev",
            account="123456789012",
            envfile=".env",
            kms_key="invalid-key"
        )
