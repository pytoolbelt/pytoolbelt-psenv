from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS

from . import (
    version,
    fetch,
    push,
    init,
    show
)


# Add your entry points / arguments in this function.....
def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    version_parser = sub_parsers.add_parser('version')
    version_parser.set_defaults(func=version.version_entrypoint)

    init_parser = sub_parsers.add_parser("init")
    init_parser.set_defaults(func=init.init_entrypoint)

    show_parser = sub_parsers.add_parser("show")
    show_parser.set_defaults(func=show.show_entrypoint)

    fetch_parser = sub_parsers.add_parser("fetch")
    fetch_parser.add_argument("-m", "--method", choices=["overwrite", "update"], default="overwrite")
    fetch_parser.add_argument("-e", "--environment", required=True)
    fetch_parser.set_defaults(func=fetch.fetch_entrypoint)

    push_parser = sub_parsers.add_parser("push")
    push_parser.set_defaults(func=push.push_entrypoint)

    return parser.parse_args()
