import pytest
from psenv.core.models import PsenvConfig, Environment, PsenvConfigError


def test_valid_psenv_config():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        root_kms_key="alias/root",
        environments=[
            Environment(name="dev", account="123456789012", envfile=".env.dev"),
            Environment(name="prod", account="987654321098", envfile=".env.prod")
        ]
    )
    assert config.envfile == ".env"
    assert config.root_path == "/params"
    assert config.root_kms_key == "alias/root"
    assert len(config.environments) == 2


def test_minimal_psenv_config():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        environments=[
            Environment(name="dev", account="123456789012", envfile=".env")
        ]
    )
    assert config.envfile == ".env"
    assert config.root_path == "/params"
    assert config.root_kms_key is None
    assert len(config.environments) == 1


def test_invalid_root_path():
    with pytest.raises(PsenvConfigError, match="Path must start with '/'"):
        PsenvConfig(
            envfile=".env",
            root_path="invalid/path",
            environments=[
                Environment(name="dev", account="123456789012", envfile=".env")
            ]
        )


def test_invalid_root_kms_key():
    with pytest.raises(PsenvConfigError, match="KMS key must start with 'alias/'"):
        PsenvConfig(
            envfile=".env",
            root_path="/params",
            root_kms_key="invalid-key",
            environments=[
                Environment(name="dev", account="123456789012", envfile=".env")
            ]
        )


def test_get_config_environment_success():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        environments=[
            Environment(name="dev", account="123456789012", envfile=".env")
        ]
    )
    env = config.get_config_environment("dev")
    assert env.environment.name == "dev"
    assert env.environment.account == "123456789012"


def test_get_config_environment_not_found():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        environments=[
            Environment(name="dev", account="123456789012", envfile=".env")
        ]
    )
    with pytest.raises(PsenvConfigError, match="Environment 'prod' not found in configuration"):
        config.get_config_environment("prod")
