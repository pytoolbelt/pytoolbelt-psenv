from argparse import Namespace
from pathlib import Path
from prettytable import PrettyTable
from psenv.core.helpers import parse_config
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile


def compare_entrypoint(cmd: Namespace) -> None:

    try:
        config = parse_config()["environments"][cmd.env]
    except KeyError:
        print(f"environment {cmd.env} not found in .psenv.yml config file.")
        exit()
    except Exception:
        print("unknown exception encountered... no idea why.")
        exit()

    parameter_store = ParameterStore(path=config["path"])
    params = parameter_store.get_parameters_by_path()
    params = parameter_store.parse_params_to_key_value_pairs(params)

    env_path = Path(config["env"])
    env_file = EnvFile(path=env_path)



