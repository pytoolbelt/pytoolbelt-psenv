from psenv.core.models import PsenvConfig, Environment, ConfigEnvironment


def test_config_environment_with_local_path():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        root_kms_key="alias/root",
        environments=[
            Environment(
                name="dev",
                account="123456789012",
                envfile=".env",
                path="/app"
            )
        ]
    )
    config_env = ConfigEnvironment(
        config=config,
        environment=config.environments[0]
    )
    assert config_env.parameter_path == "/params/dev/app"


def test_config_environment_without_local_path():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        root_kms_key="alias/root",
        environments=[
            Environment(
                name="dev",
                account="123456789012",
                envfile=".env"
            )
        ]
    )
    config_env = ConfigEnvironment(
        config=config,
        environment=config.environments[0]
    )
    assert config_env.parameter_path == "/params"


def test_config_environment_local_kms_key():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        root_kms_key="alias/root",
        environments=[
            Environment(
                name="dev",
                account="123456789012",
                envfile=".env",
                kms_key="alias/dev"
            )
        ]
    )
    config_env = ConfigEnvironment(
        config=config,
        environment=config.environments[0]
    )
    assert config_env.kms_key == "alias/dev"


def test_config_environment_inherit_root_kms_key():
    config = PsenvConfig(
        envfile=".env",
        root_path="/params",
        root_kms_key="alias/root",
        environments=[
            Environment(
                name="dev",
                account="123456789012",
                envfile=".env"
            )
        ]
    )
    config_env = ConfigEnvironment(
        config=config,
        environment=config.environments[0]
    )
    assert config_env.kms_key == "alias/root"
