from argparse import Namespace
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile
from psenv.core.config_file import ConfigFile


def push_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    env_file = EnvFile(environment["env"], template_values=False)
    params = env_file.get_params("main")

    parameter_store = ParameterStore(path=environment["path"])
    parameter_store.push_to_parameter_store(params=params, overwrite=cmd.overwrite)
