import yaml
from typing import Dict
from psenv.environment.variables import PSENV_YML


def parse_config() -> Dict[str, Dict[str, str]]:
    with PSENV_YML.open() as yml_config:
        return yaml.safe_load(yml_config)


def save_config(config: Dict[str, Dict[str, str]]) -> None:
    with PSENV_YML.open(mode="w+") as yml_config:
        yaml.dump(data=config, stream=yml_config)
