from argparse import Namespace
from psenv.core.config_file import ConfigFile
from psenv.core.parameter_store import ParameterStore
from psenv.utils.cli import validate_account, validate_admin


@validate_account
@validate_admin
def destroy_entrypoint(cmd: Namespace) -> None:
    config_file = ConfigFile()
    environment = config_file.get_environment(cmd.env)

    parameter_store = ParameterStore(path=environment["path"])
    params = parameter_store.fetch()
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
