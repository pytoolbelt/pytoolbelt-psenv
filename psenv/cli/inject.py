from argparse import Namespace
from psenv.core.helpers import get_environment_variables
from psenv.core.env_file import EnvFile
from psenv.core.config_file import ConfigFile


def inject_entrypoint(cmd: Namespace) -> None:

    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    env_file = EnvFile(environment["env"])

    # get environment vars from parent process
    params = get_environment_variables(cmd.prefix.upper())

    # update the private section of our parameters
    env_file.update_params(params=params, section="private")
    env_file.write_params()
