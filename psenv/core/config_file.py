import yaml
from pathlib import Path
from typing import Dict, Any
from psenv.environment.config import PSENV_YML


class ConfigFile:
    def __init__(self, path: Path = PSENV_YML) -> None:
        self.path = path
        self.config = self.parse_config()

    def parse_config(self) -> Dict[str, Any]:
        try:
            with self.path.open(mode="r") as yml_config:
                return yaml.safe_load(yml_config)
        except FileNotFoundError:
            print(f"psenv.yml not found in {self.path.as_posix()}")
            exit()

    def get_environment(self, env: str) -> Dict[str, Any]:
        try:
            return self.config["environments"][env]
        except KeyError:
            print(f"environment {env} not found in {self.path.as_posix()}")
            exit()

    def save_config(self) -> None:
        with self.path.open(mode="w+") as yml_config:
            yaml.dump(data=self.config, stream=yml_config)
