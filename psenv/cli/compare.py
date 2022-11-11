import shlex
from argparse import Namespace
from pathlib import Path
from tempfile import gettempdir, NamedTemporaryFile
from subprocess import Popen
from psenv.environment.variables import PSENV_COMPARE_COMMAND
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

    some_file = Path.cwd() / "some_file.env"

    some_file.touch(exist_ok=True)

    temp_file = NamedTemporaryFile()
    temp_env_path = Path(temp_file.name)

    temp_env_file = EnvFile(path=some_file)
    temp_env_file.write_params_to_env(params=params)

    command = PSENV_COMPARE_COMMAND.format(
        file1=env_file.path.absolute().as_posix(), file2=temp_env_file.path.absolute().as_posix()
    )
    command = shlex.split(command)

    process = Popen(args=command)
    output, error = process.communicate()
