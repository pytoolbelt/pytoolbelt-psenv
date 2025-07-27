from argparse import Namespace
from unittest.mock import MagicMock, patch

from psenv.cli import get


def test_configure_parser_adds_get(monkeypatch):
    subparser = MagicMock()
    parser = MagicMock()
    subparser.add_parser.return_value = parser
    get.configure_parser(subparser)
    subparser.add_parser.assert_called_once_with(
        name="get", description="Manage psenv configurations.", help="Get parameters from the parameter store."
    )
    parser.set_defaults.assert_called_once()
    parser.add_argument.assert_any_call(
        "-e",
        "--env",
        type=str,
        required=True,
    )


@patch("psenv.cli.get.Context")
def test_get_parameters_calls_context_and_envfile(mock_context):
    cliargs = Namespace(env="dev", config="foo.yml")
    mock_ctx = MagicMock()
    mock_context.from_cliargs.return_value = mock_ctx
    mock_ctx.ps_client.get_parameters.return_value = {"FOO": "bar"}
    result = get.get_parameters(cliargs)
    mock_context.from_cliargs.assert_called_once_with(cliargs)
    mock_ctx.ps_client.get_parameters.assert_called_once_with()
    mock_ctx.env_file.update_params.assert_called_once_with({"FOO": "bar"}, "main")
    mock_ctx.env_file.write_params.assert_called_once_with()
    assert result == 0


@patch("psenv.cli.get.logger")
@patch("psenv.cli.get.Context")
def test_get_parameters_logs_and_returns_0(mock_context, mock_logger):
    cliargs = Namespace(env="dev", config="foo.yml")
    mock_ctx = MagicMock()
    mock_context.from_cliargs.return_value = mock_ctx
    mock_ctx.ps_client.get_parameters.return_value = {}
    result = get.get_parameters(cliargs)
    mock_logger.info.assert_called_once_with("Fetching parameters from parameter store.", config="foo.yml")
    assert result == 0
