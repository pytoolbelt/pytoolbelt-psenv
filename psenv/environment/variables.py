import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

PSENV_HOME = Path("~/.psenv").expanduser()
PSENV_YML = PSENV_HOME / "psenv.yml"
PSENV_PUSH_EXCLUDE = os.getenv("PSENV_PUSH_EXCLUDE", "AWS_, ").split(",")
PSENV_COMPARE_COMMAND = os.getenv("PSENV_COMPARE_COMMAND", "vim -d {file1} {file2}")
