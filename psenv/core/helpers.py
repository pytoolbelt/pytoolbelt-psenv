import yaml
from typing import Dict
from psenv.environment.variables import PSENV_YML


def parse_config() -> Dict[str, str]:
    with PSENV_YML.open() as yml_config:
        return yaml.safe_load(yml_config)
