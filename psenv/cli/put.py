from argparse import Namespace
from typing import Any

import structlog

from psenv.core import diff
from psenv.core.context import Context
from psenv.core.synchronizer import Synchronizer

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
        choices=["add", "update", "sync"],
        help="The mode of operation: 'add' to add new parameters, 'update' to add new and update existing parameters. 'sync' to add new, update existing, and remove parameters that are not in the local environment file.",
    )

    put_parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Simply overwrite existing parameters in the parameter store if they exist."
    )


def put_parameters(cliargs: Namespace) -> None:
    logger.info("Putting parameters into the parameter store for environment:", config=cliargs.config)

    ctx = Context.from_cliargs(cliargs)

    # fetch the remote parameters from the parameter store
    remote_params = ctx.ps_client.get_parameters()

    # generate a parameter diff to use for the put operation
    param_diff = diff.diff_parameters(ctx.env_file.local_params, remote_params)

    synchronizer = Synchronizer(dry_run=getattr(cliargs, 'dry_run', False))
    synchronizer.sync(ctx, param_diff, mode=cliargs.mode, overwrite=cliargs.overwrite)
