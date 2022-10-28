import os
from pathlib import Path

PSENV_YML = Path(os.getenv("PSENV_YML", "~/.psenv.yml")).expanduser()
