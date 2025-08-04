import argparse
from pathlib import Path
from unittest import mock

from psenv.cli.init import configure_parser, init_entrypoint


def test_configure_parser():
    """Test that configure_parser correctly configures the init subparser."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    configure_parser(subparsers)

    # Parse args with the init command
    args = parser.parse_args(["init"])

    # Verify the command is set correctly
    assert args.command == "init"
    # Verify the function is set correctly
    assert args.func == init_entrypoint


@mock.patch("psenv.cli.init.fileio.read_config_template")
@mock.patch("psenv.cli.init.fileio.write_config")
@mock.patch("psenv.cli.init.fileio.DefaultEnvPaths")
def test_init_entrypoint(mock_default_env_paths, mock_write_config, mock_read_template):
    """Test that init_entrypoint correctly initializes a psenv project."""
    # Setup mocks
    mock_read_template.return_value = "template content"
    mock_default_env_instance = mock.MagicMock()
    mock_default_env_paths.return_value = mock_default_env_instance

    # Create args
    args = argparse.Namespace(config=Path("/test/path/psenv.yml"))

    # Call the function
    init_entrypoint(args)

    # Verify the template was read
    mock_read_template.assert_called_once()

    # Verify the config was written
    mock_write_config.assert_called_once_with(args.config, "template content")

    # Verify the DefaultEnvPaths was instantiated with the correct path
    mock_default_env_paths.assert_called_once_with(args.config)

    # Verify the create method was called
    mock_default_env_instance.create.assert_called_once()


@mock.patch("psenv.cli.init.fileio.read_config_template")
@mock.patch("psenv.cli.init.fileio.write_config")
@mock.patch("psenv.cli.init.fileio.DefaultEnvPaths")
def test_init_entrypoint_with_existing_config(mock_default_env_paths, mock_write_config, mock_read_template, tmp_path):
    """Test that init_entrypoint works when config file already exists."""
    # Setup mocks
    mock_read_template.return_value = "template content"
    mock_default_env_instance = mock.MagicMock()
    mock_default_env_paths.return_value = mock_default_env_instance

    # Create a temporary config file
    config_path = tmp_path / "psenv.yml"
    config_path.write_text("existing config")

    # Create args
    args = argparse.Namespace(config=config_path)

    # Call the function
    init_entrypoint(args)

    # Verify all the expected calls were made
    mock_read_template.assert_called_once()
    mock_write_config.assert_called_once_with(config_path, "template content")
    mock_default_env_paths.assert_called_once_with(config_path)
    mock_default_env_instance.create.assert_called_once()
