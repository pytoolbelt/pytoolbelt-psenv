import boto3
from typing import Callable, Any
from psenv.environment.variables import PSENV_AWS_ACCOUNT_ID, PSENV_AWS_ARN_NAME


def validate_account(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        sts = boto3.client("sts")
        account_id = int(sts.get_caller_identity()["Account"])

        if account_id != PSENV_AWS_ACCOUNT_ID:
            print(f"psenv expects account {PSENV_AWS_ACCOUNT_ID} but account is {account_id}")
            exit(1)
        return func(*args, **kwargs)

    return wrapper


def validate_admin(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        sts = boto3.client("sts")
        arn = sts.get_caller_identity()["Arn"]
        _, name, _ = arn.partition(PSENV_AWS_ARN_NAME)

        if name != PSENV_AWS_ARN_NAME:
            print(f"psenv admin operation. You do not have the jam to perform this operation!")
            exit(1)
        return func(*args, **kwargs)

    return wrapper


def yes_no_confirmation(msg: str) -> None:

    while True:

        selection = input(f"{msg} : Are you sure? : [y/n] -> ").lower()

        if selection not in ["y", "n"]:
            print("please make a valid selection.")
        elif selection == "y":
            break
        elif selection == "n":
            exit(0)
        else:
            print("Invalid selection.")
            exit(1)
