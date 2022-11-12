from argparse import Namespace
from psenv.core.config_file import ConfigFile


def new_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()

    new_entry = {cmd.env: {"path": cmd.path, "env": cmd.file}}

    config_file.config["environments"].update(**new_entry)
    config_file.save_config()
