from argparse import Namespace
from pathlib import Path
from psenv.core.parameter_store import ParameterStore
from psenv.core.config_file import ConfigFile
from psenv.core.env_file import EnvFile


def fetch_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    parameter_store = ParameterStore(path=environment["path"])
    params = parameter_store.get_parameters_by_path()
    params = parameter_store.parse_params_to_key_value_pairs(params)

    env_path = Path(environment["env"]).expanduser()
    env_file = EnvFile(path=env_path)

    print(f"writing params to {env_path.as_posix()}")
    env_file.write_params_to_env(params=params, method=cmd.method)

    if cmd.method == "update":
        print("updating private .env")
        env_file.append_private_section()
