"""
Project version command used to simply display the version to the terminal.
The __version__ variable value is managed by the semantic-release package
and should not be manually adjusted by a developer.
"""

from argparse import Namespace

__version__ = "0.17.1"


def version_entrypoint(cmd: Namespace) -> None:
    print(f"psenv -- Version : {__version__}")
