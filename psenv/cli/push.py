from argparse import Namespace
from pathlib import Path
from psenv.core.helpers import parse_config
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile


def push_entrypoint(cmd: Namespace) -> None:
    config = parse_config()["environments"][cmd.env]

    env_path = Path(config["env"]).expanduser()
    env_file = EnvFile(path=env_path)

    parameter_store = ParameterStore(path=config["path"])
    parameter_store.push_to_parameter_store(params=env_file.main_content, overwrite=cmd.overwrite)
