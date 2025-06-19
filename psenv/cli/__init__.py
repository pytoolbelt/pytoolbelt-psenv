from argparse import ArgumentParser, Namespace
from importlib import metadata
from pathlib import Path
from types import ModuleType
from typing import List

from psenv.paths import PSENV_CONFIG_FILE_PATH

from . import config, get, put

COMMANDS = [config, get, put]


def commands() -> List[ModuleType]:
    return sorted(COMMANDS, key=lambda x: x.__name__)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"psenv :: {metadata.version('psenv')} :: AWS Parameter Store Environment Manager",
    )

    parser.add_argument(
        "-c",
        "--config",
        help="Path to the psenv configuration file.",
        type=Path,
        required=False,
        default=PSENV_CONFIG_FILE_PATH,
        metavar="",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    for command in commands():
        command.configure_parser(subparsers)

    return parser.parse_args()
