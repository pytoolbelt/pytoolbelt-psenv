from pathlib import Path

PSENV_HOME = Path("~/.psenv").expanduser()
PSENV_YML = PSENV_HOME / "psenv.yml"
PSENV_ENV_FILE = PSENV_HOME / "psenv.env"
PSENV_TEMPLATE_PREFIX = "PSENV__TEMPLATE__"
PSENV_PRIVATE_MARKER = "#<private>"
