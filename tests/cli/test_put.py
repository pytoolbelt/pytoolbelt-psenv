from argparse import Namespace
from unittest.mock import MagicMock, patch

from psenv.cli import put
from psenv.core.diff import ParameterDiff


def test_configure_parser_adds_put():
    subparser = MagicMock()
    parser = MagicMock()
    subparser.add_parser.return_value = parser
    put.configure_parser(subparser)

    # Verify parser setup
    subparser.add_parser.assert_called_once_with(
        name="put", description="Manage psenv configurations.", help="Put parameters into the parameter store."
    )
    parser.set_defaults.assert_called_once_with(func=put.put_parameters)

    # Verify arguments
    parser.add_argument.assert_any_call("-e", "--env", type=str, required=True, help="The environment to put parameters for.", metavar="")

    # Verify mutually exclusive group arguments
    group = parser.add_mutually_exclusive_group.return_value
    group.add_argument.assert_any_call("-a", "--add", action="store_true", help="Add new parameters only.")
    group.add_argument.assert_any_call("-u", "--update", action="store_true", help="Add new and update existing parameters.")
    group.add_argument.assert_any_call(
        "-s", "--sync", action="store_true", help="Add new, update existing, and remove parameters not in the local environment file."
    )

    # Verify dry-run
    parser.add_argument.assert_any_call("--dry-run", action="store_true", help="Show what would be done, but do not make any changes.")


@patch("psenv.cli.put.Synchronizer")
@patch("psenv.cli.put.Context")
@patch("psenv.cli.put.diff.diff_parameters")
def test_put_parameters_calls_synchronizer(mock_diff, mock_context, mock_synchronizer):
    # Setup mocks
    cliargs = Namespace(config="config.yml", env="dev", add=True, update=False, sync=False, dry_run=False)

    mock_ctx = MagicMock()
    mock_context.from_cliargs.return_value = mock_ctx

    mock_ctx.env_file.local_params = {"FOO": "bar"}
    mock_ctx.ps_client.get_parameters.return_value = {"BAZ": "qux"}

    mock_param_diff = MagicMock(spec=ParameterDiff)
    mock_diff.return_value = mock_param_diff

    mock_sync = MagicMock()
    mock_synchronizer.return_value = mock_sync

    # Call function under test
    put.put_parameters(cliargs)

    # Verify calls
    mock_context.from_cliargs.assert_called_once_with(cliargs)
    mock_ctx.ps_client.get_parameters.assert_called_once()
    mock_diff.assert_called_once_with(mock_ctx.env_file.local_params, mock_ctx.ps_client.get_parameters())

    # Verify Synchronizer was created with correct args
    mock_synchronizer.assert_called_once()
    args, kwargs = mock_synchronizer.call_args
    assert kwargs["ctx"] == mock_ctx
    assert kwargs["param_diff"] == mock_param_diff

    # Verify sync was called
    mock_sync.sync.assert_called_once()


@patch("psenv.cli.put.Synchronizer")
@patch("psenv.cli.put.Context")
@patch("psenv.cli.put.diff.diff_parameters")
def test_put_parameters_dry_run(mock_diff, mock_context, mock_synchronizer):
    # Setup with dry_run=True
    cliargs = Namespace(config="config.yml", env="dev", add=False, update=False, sync=True, dry_run=True)

    mock_ctx = MagicMock()
    mock_context.from_cliargs.return_value = mock_ctx

    mock_ctx.env_file.local_params = {"FOO": "bar"}
    mock_ctx.ps_client.get_parameters.return_value = {"BAZ": "qux"}

    mock_param_diff = MagicMock(spec=ParameterDiff)
    mock_diff.return_value = mock_param_diff

    mock_sync = MagicMock()
    mock_synchronizer.return_value = mock_sync

    # Call function
    put.put_parameters(cliargs)

    # Verify Synchronizer was created with dry_run=True
    mock_synchronizer.assert_called_once()
    args, kwargs = mock_synchronizer.call_args
    assert kwargs["dry_run"] == True
