import os

PSENV_RAISE_ERRORS = os.getenv("PSENV_RAISE_ERRORS", "false").lower() == "true"
PSENV_PRIVATE_MARKER = "#<private>"
