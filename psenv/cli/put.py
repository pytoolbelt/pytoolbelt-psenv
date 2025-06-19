from argparse import Namespace
from typing import Any

import structlog

from psenv import aws, fileio, diff
from psenv.models import load_config
from pathlib import Path
logger = structlog.get_logger(__name__)


def configure_parser(subparser: Any) -> None:
    put_parser = subparser.add_parser(
        name="put", description="Manage psenv configurations.", help="Put parameters into the parameter store."
    )
    put_parser.set_defaults(func=put_parameters)

    put_parser.add_argument("-e", "--env", type=str, required=True, help="The environment to put parameters for.")

    put_parser.add_argument(
        "-m",
        "--mode",
        type=str,
        required=False,
        default="add",
        choices=["add", "sync"],
        help="The mode of operation: 'add' to add new parameters, 'sync' to synchronize existing ones.",
    )

    put_parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Simply overwrite existing parameters in the parameter store if they exist."
    )


def put_parameters(cliargs: Namespace) -> None:
    logger.info("Putting parameters into the parameter store for environment:", config=cliargs.config)
    config = load_config(cliargs.config)

    config_env = config.get_config_environment(cliargs.env)

    sts = aws.StsClient()
    sts.raise_if_invalid_account(config_env.environment.account)

    env_file = fileio.EnvFile(Path(config_env.environment.envfile))
    env_file.load()

    ps_client = aws.ParameterStoreClient(parameter_path=config_env.parameter_path, kms_key=config_env.kms_key)
    remote_params = ps_client.get_parameters()

    param_diff = diff.diff_parameters(env_file.local_params, remote_params)

    if cliargs.mode == "sync":
        logger.info("Syncing parameters with the parameter store.")
        ps_client.put_parameters(param_diff.to_add)

        ps_client.put_parameters(param_diff.to_update)

        logger.info("Removing parameters that are not in the local environment file.")
        ps_client.delete_parameters(param_diff.to_remove)

