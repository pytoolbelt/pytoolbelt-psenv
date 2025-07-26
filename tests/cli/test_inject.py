from argparse import Namespace
from unittest.mock import patch, MagicMock
from psenv.cli import inject

def test_configure_parser_adds_inject():
    subparser = MagicMock()
    parser = MagicMock()
    subparser.add_parser.return_value = parser
    inject.configure_parser(subparser)
    subparser.add_parser.assert_called_once_with(
        name="inject",
        description="Inject environment variables from your session to an .env file",
        help="Inject environment variables to an .env file",
    )
    parser.set_defaults.assert_called_once_with(func=inject.inject_parameters)
    parser.add_argument.assert_any_call(
        "-e", "--env", type=str, required=False, help="The environment to inject parameters to."
    )
    parser.add_argument.assert_any_call(
        "-p", "--prefix", type=str, required=False, default="", help="The prefix to filter environment variables by."
    )

@patch("psenv.cli.inject.get_environment_variables")
@patch("psenv.cli.inject.EnvFile")
@patch("psenv.cli.inject.load_config")
@patch("psenv.cli.inject.logger")
def test_inject_parameters_calls_dependencies(mock_logger, mock_load_config, mock_envfile, mock_get_env_vars):
    cliargs = Namespace(config="foo.yml", prefix="FOO")
    mock_config = MagicMock()
    mock_config.envfile = "bar.env"
    mock_load_config.return_value = mock_config
    mock_env_file_instance = MagicMock()
    mock_envfile.return_value = mock_env_file_instance
    mock_get_env_vars.return_value = {"FOO_BAR": "baz"}

    inject.inject_parameters(cliargs)

    mock_logger.info.assert_called_once_with(
        "Putting parameters into the parameter store for environment:", config="foo.yml"
    )
    mock_load_config.assert_called_once_with("foo.yml")
    mock_envfile.assert_called_once()
    mock_get_env_vars.assert_called_once_with("FOO")
    mock_env_file_instance.update_params.assert_called_once_with({"FOO_BAR": "baz"}, section="private")
    mock_env_file_instance.write_params.assert_called_once_with()

