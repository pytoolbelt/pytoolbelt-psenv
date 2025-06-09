from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ValidationError, field_validator

from psenv.paths import PSENV_CONFIG_FILE_PATH
from psenv.error_handling.exceptions import PsenvConfigError
from psenv.fileio import read_config


# TODO: kms key should be a regex pattern
class Environment(BaseModel):
    name: str
    account: str  #TODO: regex this for aws account id
    envfile: str
    kms_key: Optional[str] = None
    path: Optional[str]

    @field_validator("account")
    def validate_account(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 12:
            raise ValueError("AWS account ID must be a 12-digit numeric string.")
        return value

class PsenvConfig(BaseModel):
    envfile: str
    root_path: str
    root_kms_key: Optional[str] = None
    environments: List[Environment]

    def get_environment(self, name: str) -> Environment:
        for env in self.environments:
            if env.name == name:
                return env
        raise PsenvConfigError(f"Environment '{name}' not found in configuration.")

def load_config(path: Optional[Path] = None) -> PsenvConfig:
    path = path or PSENV_CONFIG_FILE_PATH
    config = read_config(path)
    try:
        return PsenvConfig.model_validate(config)
    except ValidationError as e:
        raise PsenvConfigError("Error loading config") from e
