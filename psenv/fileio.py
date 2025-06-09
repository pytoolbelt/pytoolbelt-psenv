import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from psenv.error_handling.exceptions import PsenvConfigNotFoundError, PsenvConfigError, PsenvInternalError
from psenv.paths import PSENV_TEMPLATE_FILE_PATH

def read_config(path: Path) -> Dict[str, Any]:
    path = path.absolute()
    try:
        content = os.path.expandvars(path.read_text())
        return yaml.safe_load(content)
    except FileNotFoundError:
        raise PsenvConfigNotFoundError(f"psenv.yml not found in {path.as_posix()}. Please check the path or create a new configuration file.")
    except yaml.YAMLError as e:
        raise PsenvConfigError("Error loading psenv.yml") from e


def read_config_template(path: Optional[Path] = None) -> str:
    path = path or PSENV_TEMPLATE_FILE_PATH
    try:
        return path.absolute().read_text()
    except FileNotFoundError:
        raise PsenvInternalError(f"psenv template file not found at {path}. Please file a bug report.")

def write_config(path: Path, content: str) -> None:
    path = path.absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    path.write_text(content)
