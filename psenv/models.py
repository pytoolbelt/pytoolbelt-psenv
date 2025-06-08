from pathlib import Path

from pydantic import BaseModel, ValidationError
from typing import List, Optional
from psenv.fileio import read_config
from psenv.config import PSENV_CONFIG_FILE_PATH
from psenv.error_handling.exceptions import PsenvConfigError


class Environment(BaseModel):
    name: str
    account: int
    envfile: str
    path: Optional[str]


class PsenvConfig(BaseModel):
    envfile: str
    root_path: str
    environments: List[Environment]


def load_config(path: Optional[Path] = None) -> PsenvConfig:
    path = path or PSENV_CONFIG_FILE_PATH
    config = read_config(path)
    try:
        return PsenvConfig.model_validate(config)
    except ValidationError:
        raise PsenvConfigError()


