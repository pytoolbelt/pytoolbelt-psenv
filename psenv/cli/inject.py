from argparse import Namespace
from typing import Any

import structlog

from psenv.context import Context
from psenv.fileio import get_environment_variables

logger = structlog.get_logger(__name__)


def configure_parser(subparser: Any) -> None:
    inject_parser = subparser.add_parser(
        name="inject", description="Inject environment variables from your session to an .env file", help="Inject environment variables to an .env file"
    )
    inject_parser.set_defaults(func=inject_parameters)

    inject_parser.add_argument("-e", "--env", type=str, required=False, help="The environment to inject parameters to.")
    inject_parser.add_argument("-p", "--prefix", type=str, required=False, default="", help="The prefix to filter environment variables by.")

def inject_parameters(cliargs: Namespace) -> None:
    logger.info("Putting parameters into the parameter store for environment:", config=cliargs.config)

    ctx = Context.from_cliargs(cliargs)

    env_vars = get_environment_variables(cliargs.prefix)
    ctx.env_file.update_params(env_vars, section="private")
    ctx.env_file.write_params()
