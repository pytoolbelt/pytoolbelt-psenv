from argparse import Namespace, REMAINDER
from typing import Any
from psenv.command import Command
import structlog

logger = structlog.get_logger(__name__)


def configure_parser(subparser: Any) -> None:
    put_parser = subparser.add_parser(
        name="exec",
        description="Run a parameterized command",
        help="Execute a command with parameters from the parameter store."
    )
    put_parser.set_defaults(func=exec_command)

    put_parser.add_argument("-e", "--env", type=str, required=True, help="The environment to run the command for.")
    put_parser.add_argument("command", nargs=REMAINDER, help="Command to execute with its arguments")

def exec_command(cliargs: Namespace) -> None:
    print("Executing command with parameters")
    print(cliargs)

    with Command(cliargs.command):
        pass
