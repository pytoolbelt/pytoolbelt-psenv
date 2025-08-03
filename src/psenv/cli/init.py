from argparse import Namespace, Action
from pathlib import Path
from typing import Any
import structlog

from psenv.core import fileio
from psenv.core.paths import PSENV_CONFIG_FILE_PATH
from psenv.error_handling.exceptions import PsenvConfigError

logger = structlog.get_logger(__name__)


class ValidatePathAction(Action):
    def __call__(self, parser, namespace, values: Path, option_string=None):
        if not values.suffix:
            raise PsenvConfigError(f"Path is not a file: {values}")
        if not values.suffix == ".yml":
            raise PsenvConfigError(f"Invalid file type: {values.suffix}. Expected a .yml file.")
        if values.exists():
            raise PsenvConfigError(f"Psenv config file already exists: {values}")
        setattr(namespace, self.dest, values)


def configure_parser(subparser: Any) -> None:
    init_parser = subparser.add_parser(name="init", description="Manage psenv configurations.")
    init_parser.set_defaults(func=init_entrypoint)

    init_parser.add_argument(
        "-p",
        "--path",
        help="Path to the new configuration file.",
        type=Path,
        required=False,
        default=PSENV_CONFIG_FILE_PATH,
        action=ValidatePathAction,
    )


def init_entrypoint(cliargs: Namespace) -> None:
    logger.info("Creating new psenv configuration file")
    template = fileio.read_config_template()
    fileio.write_config(cliargs.path, template)

    logger.info("Creating new psenv environment directory")
    default_env = fileio.DefaultEnvPaths(cliargs.path)
    default_env.create()
