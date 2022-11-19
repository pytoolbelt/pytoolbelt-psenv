from argparse import Namespace
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile
from psenv.core.config_file import ConfigFile
from psenv.utils.cli import validate_account, validate_admin


@validate_account
@validate_admin
def push_entrypoint(cmd: Namespace) -> None:

    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    env_file = EnvFile(environment["env"], template_values=False)
    params = env_file.get_params("main")

    parameter_store = ParameterStore(path=environment["path"])
    responses = parameter_store.push(params=params, overwrite=cmd.overwrite)

    for response in responses:
        print(response)
