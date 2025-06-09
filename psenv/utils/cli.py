from typing import Any, Callable

import boto3

from psenv.environment.variables import PSENV_AWS_ACCOUNT_ID


def validate_account(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        sts = boto3.client("sts")
        account_id = int(sts.get_caller_identity()["Account"])

        if account_id != PSENV_AWS_ACCOUNT_ID:
            print(f"psenv expects account {PSENV_AWS_ACCOUNT_ID} but account is {account_id}")
            exit(1)
        return func(*args, **kwargs)

    return wrapper
