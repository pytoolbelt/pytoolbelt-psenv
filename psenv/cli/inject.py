from argparse import Namespace
from pathlib import Path
from psenv.core.helpers import get_environment_variables
from psenv.core.env_file import EnvFile
from psenv.core.config_file import ConfigFile


def inject_entrypoint(cmd: Namespace) -> None:

    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    env_path = Path(environment["env"]).expanduser()
    env_file = EnvFile(env_path)

    # get environment vars from parent process
    params = get_environment_variables(cmd.prefix.upper())

    if params:
        env_file.private_content.update(**params)
        env_file.write_params_to_env(params=env_file.main_content, method="update")
        env_file.append_private_section()
    else:
        print(f"no params found in environment with prefix {cmd.prefix}")
