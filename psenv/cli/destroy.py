from argparse import Namespace
from psenv.core.config_file import ConfigFile
from psenv.core.parameter_store import ParameterStore
from psenv.core.env_file import EnvFile


def destroy_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    parameter_store = ParameterStore(path=environment["path"])
    env_file = EnvFile(environment["env"])

    params = env_file.get_params("main")
    delete_generator = parameter_store.delete(params)

    while True:

        try:
            responses = next(delete_generator)
        except StopIteration:
            break

        try:
            for response in responses["DeletedParameters"]:
                print(f"Deleted Parameter -- {response}")
        except KeyError:
            print("No parameters found to delete")

        try:
            for response in responses["InvalidParameters"]:
                print(f"Parameter Invalid -- {response}")
        except KeyError:
            print("All delete requests were valid")
