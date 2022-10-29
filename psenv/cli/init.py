from argparse import Namespace
from psenv.environment.variables import PSENV_YML, PSENV_HOME


def init_entrypoint(cmd: Namespace) -> None:
    PSENV_HOME.mkdir(exist_ok=True)
    PSENV_YML.touch(exist_ok=True)
