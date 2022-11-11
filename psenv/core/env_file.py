from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import dotenv_values

PRIVATE_MARKER = "#<private>"


class EnvFile:
    def __init__(self, path: Path) -> None:
        self.path = path

        # set up main and private content
        content = self.path.read_text().partition(PRIVATE_MARKER)
        self.main_content = self._parse_values_to_dict(content[0])
        self.private_content = self._parse_values_to_dict(content[2])

        self._methods = {"overwrite": self._overwrite_env, "update": self._update_env}

    @staticmethod
    def _parse_values_to_dict(content: str) -> Dict[str, str]:
        with StringIO() as buffer:
            buffer.write(content)
            buffer.seek(0)
            return dotenv_values(stream=buffer)

    @staticmethod
    def _get_sorted_keys(params: Dict[str, str]) -> List[str]:
        return sorted(params.keys())

    def _overwrite_env(self, params: Dict[str, str], mode: str = "w+", extra: Optional[str] = None) -> None:
        keys = self._get_sorted_keys(params)

        with self.path.open(mode=mode) as env:
            if extra:
                env.write(extra)

            ref_prefix = ""
            for key in keys:

                current_prefix = key.split("_")[0]
                if current_prefix != ref_prefix:
                    ref_prefix = current_prefix
                    env.write("\n")
                    env.write(f"# ----------------------------{current_prefix}------------------------------------ #\n")

                value = params[key]
                line = f"{key}={value}"
                env.write(f"{line}\n")

    def _update_env(self, params: Dict[str, str] = None) -> None:
        self.main_content.update(**params)
        self._overwrite_env(self.main_content)

    def write_params_to_env(self, params: Dict[str, str], method: str = "overwrite") -> None:

        if method not in self._methods.keys():
            raise ValueError(f"available methods are {self._methods.keys()} got {method} instead")

        method = self._methods.get(method)
        method(params=params)

    def append_private_section(self) -> None:
        extra = f"\n\n{PRIVATE_MARKER}\n\n"
        self._overwrite_env(params=self.private_content, mode="a", extra=extra)
