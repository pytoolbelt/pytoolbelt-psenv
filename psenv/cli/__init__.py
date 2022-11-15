from argparse import ArgumentParser
from psenv.cli import version, fetch, push, init, show, validation, inject, new, destroy


# Add your entry points / arguments in this function.....
def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="command")
    sub_parsers.required = True

    version_parser = sub_parsers.add_parser("version", help="Display the current version of psenv")
    version_parser.set_defaults(func=version.version_entrypoint)

    init_parser = sub_parsers.add_parser("init", help="Init psenv")
    init_parser.set_defaults(func=init.init_entrypoint)

    show_parser = sub_parsers.add_parser("show", help="Print configured environments to the terminal")
    show_parser.set_defaults(func=show.show_entrypoint)

    fetch_parser = sub_parsers.add_parser("fetch", help="Fetch parameters from the AWS Parameter Store")
    fetch_parser.add_argument("-m", "--method", choices=["overwrite", "update"], default="update")
    fetch_parser.set_defaults(func=fetch.fetch_entrypoint)

    push_parser = sub_parsers.add_parser("push", help="Push parameters to the AWS Parameter Store")
    push_parser.set_defaults(func=push.push_entrypoint)
    push_parser.add_argument(
        "-o", "--overwrite", default=False, action="store_true", help="overwrite existing parameter store values"
    )

    new_parser = sub_parsers.add_parser("new", help="Create a new psenv environment")
    new_parser.add_argument("-f", "--file", action=validation.ValidateFileName)
    new_parser.set_defaults(func=new.new_entrypoint)

    destroy_parser = sub_parsers.add_parser("destroy", help="NOT YET IMPLEMENTED")
    destroy_parser.set_defaults(func=destroy.destroy_entrypoint)

    inject_parser = sub_parsers.add_parser("inject", help="Inject variables from current session to a .env file")
    inject_parser.set_defaults(func=inject.inject_entrypoint)
    inject_parser.add_argument("-p", "--prefix", help="target environment variables with this prefix.", required=True)

    # adding the environment flag to necessary commands
    for p in fetch_parser, push_parser, new_parser, destroy_parser, inject_parser:
        p.add_argument(
            "-e",
            "--env",
            required=True,
            action=validation.ValidateEnvironmentName,
            help="name of the configured environment",
        )

    # adding the path flag to necessary commands
    for p in new_parser, destroy_parser:
        p.add_argument("-p", "--path", action=validation.ValidatePathName, help="variable path in the parameter store")
    return parser.parse_args()
