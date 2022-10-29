from argparse import Namespace
from psenv.core.helpers import parse_config
from psenv.core.env_file import EnvFile
from psenv.core.parameter_store import ParameterStore

def push_entrypoint(cmd: Namespace) -> None:
    print("push entrypoint")
