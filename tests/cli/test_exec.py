from argparse import Namespace
from unittest.mock import MagicMock, patch

from psenv.cli import exec as exec_mod


def test_configure_parser_adds_exec():
    subparser = MagicMock()
    parser = MagicMock()
    subparser.add_parser.return_value = parser
    exec_mod.configure_parser(subparser)
    subparser.add_parser.assert_called_once_with(
        name="exec", description="Run a parameterized command", help="Execute a command with parameters from the parameter store."
    )
    parser.set_defaults.assert_called_once_with(func=exec_mod.exec_command)
    parser.add_argument.assert_any_call("-e", "--env", type=str, required=True, help="The environment to run the command for.")
    parser.add_argument.assert_any_call("command", nargs=exec_mod.REMAINDER, help="Command to execute with its arguments")


@patch("psenv.cli.exec.Command")
@patch("psenv.cli.exec.Context")
def test_exec_command_calls_context_and_command(mock_context, mock_command):
    cliargs = Namespace(env="dev", config="foo.yml", command=["echo", "hi"])
    mock_ctx = MagicMock()
    mock_context.from_cliargs.return_value = mock_ctx
    mock_ctx.ps_client.get_parameters.return_value = {"FOO": "bar"}
    mock_cm = MagicMock()
    mock_command.return_value.__enter__.return_value = mock_cm
    result = exec_mod.exec_command(cliargs)
    mock_context.from_cliargs.assert_called_once_with(cliargs)
    mock_ctx.ps_client.get_parameters.assert_called_once_with()
    mock_command.assert_called_once_with(["echo", "hi"], env={"FOO": "bar"})
    # Should print the execution message
    # result is None (function returns None)
    assert result is None
