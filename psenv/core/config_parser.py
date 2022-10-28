import yaml
from typing import Dict
from psenv.environment.variables import PSENV_YML


def parse_config() -> Dict[str, str]:

    if not PSENV_YML.exists():
        raise FileNotFoundError("a config file must exist in either ~/.psenv.yml, or specified in PSENV_YML")

    return yaml.safe_load(PSENV_YML.open())
