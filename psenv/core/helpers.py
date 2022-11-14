import os
from typing import Dict


def get_environment_variables(prefix: str) -> Dict[str, str]:
    retrieved = {}
    prefix = prefix.upper()
    for key, value in os.environ.items():
        if key.startswith(prefix):
            retrieved[key] = value
    return retrieved
