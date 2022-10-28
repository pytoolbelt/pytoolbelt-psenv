from argparse import Namespace
from prettytable import PrettyTable
from psenv.core.config_parser import parse_config


def show_entrypoint(cmd: Namespace) -> None:
    print("fetch entrypoint")

    config = parse_config()

    table = PrettyTable()
    table.field_names = ["environment", "parameter store path", "local env file path"]

    for key, value in config["environments"].items():
        row = [key, value["path"], value["env"]]
        table.add_row(row)

    print(table)
