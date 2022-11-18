from io import StringIO
from pathlib import Path
from typing import Dict, TextIO
from dotenv import dotenv_values
from psenv.environment.config import PSENV_TEMPLATE_PREFIX, PSENV_PRIVATE_MARKER


class EnvFile:
    def __init__(self, path: str, template_values: bool = True) -> None:
        self.path = Path(path).expanduser()
        self.template_values = template_values
        self._main_params = {}
        self._private_params = {}
        self._template_params = {}
        self._prefix = ""

        if not self.path.exists():
            self.path.touch()

        # read file and parse out sections if they exist
        mp, _, pp = self.path.read_text().partition(PSENV_PRIVATE_MARKER)
        with StringIO() as stream:
            stream.write(mp)
            stream.seek(0)
            self._main_params = dotenv_values(stream=stream)

        with StringIO() as stream:
            stream.write(pp)
            stream.seek(0)
            self._private_params = dotenv_values(stream=stream)

        if self.template_values:
            self._process_template_params()

    def _process_template_params(self) -> None:
        template_keys = [key for key in self._main_params.keys() if key.startswith(PSENV_TEMPLATE_PREFIX)]

        for template_key in template_keys:
            template_value = self._main_params.pop(template_key)
            private_key = template_key.lstrip(PSENV_TEMPLATE_PREFIX)

            if private_key not in self._private_params.keys():
                self._private_params.update(**{private_key: template_value})

    def _write_param_to_file(self, key: str, value: str, env: TextIO) -> None:

        prefix = key.split("_")[0]
        if prefix != self._prefix:
            self._prefix = prefix
            env.write("\n")
            env.write(f"# ----------------------------{self._prefix}------------------------------------ #\n")

        line = f"{key}={value}"
        env.write(f"{line}\n")

    def get_params(self, section: str) -> Dict[str, str]:
        return getattr(self, f"_{section}_params", {})

    def update_params(self, params: Dict[str, str], section: str, template_params: bool = False) -> None:
        p = self.get_params(section)
        p.update(**params)
        setattr(self, f"_{section}_params", p)

        if template_params:
            self._process_template_params()

    def write_params(self) -> None:
        self._prefix = ""

        with self.path.open(mode="w+") as env:
            for section in "main", "private":
                params = self.get_params(section)
                keys = sorted(params.keys())

                if section == "private":
                    env.write(f"\n\n{PSENV_PRIVATE_MARKER}\n\n")

                for key in keys:
                    value = params[key]
                    self._write_param_to_file(key, value, env)
