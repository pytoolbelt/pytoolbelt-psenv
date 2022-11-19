import os
from dotenv import load_dotenv
from psenv.environment.config import PSENV_ENV_FILE

load_dotenv(dotenv_path=PSENV_ENV_FILE)

PSENV_AWS_ACCOUNT_ID = int(os.getenv("PSENV_AWS_ACCOUNT_ID", 0))
PSENV_AWS_ARN_NAME = os.getenv("PSENV_AWS_ARN_NAME", None)
