from argparse import Namespace
from prettytable import PrettyTable
from psenv.core.config_file import ConfigFile


def show_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()

    table = PrettyTable()
    table.field_names = ["environment", "parameter store path", "local env file path"]

    for key, value in config_file.config["environments"].items():
        row = [key, value["path"], value["env"]]
        table.add_row(row)

    print(table)
