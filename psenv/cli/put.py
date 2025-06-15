from argparse import ArgumentParser, Namespace
from typing import Any


def configure_parser(subparser: Any) -> None:
    put_parser = subparser.add_parser(
        name="put",
        description="Manage psenv configurations.",
        help="Put parameters into the parameter store."
    )
    put_parser.set_defaults(func=put_parameters)

    put_parser.add_argument(
        "-e",
        "--env",
        type=str,
        required=True,
        help="The environment to put parameters for."
    )

    put_parser.add_argument(
        "-m",
        "--mode",
        type=str,
        required=False,
        default="add",
        choices=["add", "sync"],
        help="The mode of operation: 'add' to add new parameters, 'sync' to synchronize existing ones."
    )

    put_parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Simply overwrite existing parameters in the parameter store if they exist."
    )

def put_parameters(cliargs: Namespace) -> None:
    print("Putting parameters into the parameter store for environment:", cliargs)


