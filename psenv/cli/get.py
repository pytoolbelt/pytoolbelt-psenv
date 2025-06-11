from argparse import Namespace
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
import structlog
from psenv.models import load_config
from psenv import aws, fileio

logger = structlog.get_logger(__name__)


def configure_parser(subparser: Any) -> None:
    get_parser = subparser.add_parser(name="get", description="Manage psenv configurations.", help="Get parameters from the parameter store.")
    get_parser.set_defaults(func=get_parameters)

    get_parser.add_argument(
        "-e",
        "--env",
        type=str,
        required=True,
    )


def get_parameters(cliargs: Namespace) -> int:
    logger.info("Fetching parameters from parameter store.", config=cliargs.config)
    config = load_config(cliargs.config)

    # load environment variables from .env file
    load_dotenv(config.envfile)

    # Fetch config for the specified environment
    env = config.get_config_environment(cliargs.env)

    # if we are not in the expected account from the parent session, raise an error
    sts = aws.StsClient()
    sts.raise_if_invalid_account(env.account)

    # Fetch parameters from the parameter store
    parameters = aws.ParameterStoreClient(parameter_path=env.parameter_path, kms_key=env.kms_key).get_parameters()

    env_file = fileio.EnvFile(Path(env.envfile))
    env_file.load()

    env_file.update_params(parameters, "main")
    env_file.write_params()
    return 0
