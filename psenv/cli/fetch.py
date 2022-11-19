from argparse import Namespace
from psenv.core.parameter_store import ParameterStore
from psenv.core.config_file import ConfigFile
from psenv.core.env_file import EnvFile
from psenv.utils.cli import validate_account


@validate_account
def fetch_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    parameter_store = ParameterStore(path=environment["path"])
    params = parameter_store.fetch()

    if not params:
        print(f"No params found in the parameter store on path {environment['path']}")
        exit()

    env_file = EnvFile(environment["env"])

    if cmd.method == "overwrite":
        print(f"Overwriting {env_file.path.as_posix()}")
        with env_file.path.open(mode="w+") as env:
            env.truncate()

        for section in "main", "private", "template":
            env_file.clear_params(section)

    env_file.update_params(params=params, section="main", template_params=cmd.no_template)

    env_file.write_params()
    print(f"Params written to {env_file.path.as_posix()}")
