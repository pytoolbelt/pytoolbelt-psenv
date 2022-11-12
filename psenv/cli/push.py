from argparse import Namespace
from pathlib import Path
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile
from psenv.core.config_file import ConfigFile


def push_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    env_path = Path(environment["env"]).expanduser()
    env_file = EnvFile(path=env_path)

    parameter_store = ParameterStore(path=environment["path"])
    parameter_store.push_to_parameter_store(params=env_file.main_content, overwrite=cmd.overwrite)
