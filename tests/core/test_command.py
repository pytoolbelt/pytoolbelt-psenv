from unittest.mock import MagicMock, patch

import pytest

from psenv.core.command import Command


@patch("psenv.core.command.Popen.__init__", return_value=None)
def test_command_init_removes_double_dash(mock_popen_init):
    cmd = ["--", "echo", "hello"]
    c = Command(cmd)
    assert c.command == ["echo", "hello"]
    mock_popen_init.assert_called_once()


@patch("psenv.core.command.Popen.__init__", return_value=None)
def test_command_init_env_default(mock_popen_init):
    cmd = ["echo", "hello"]
    c = Command(cmd)
    assert c.command == ["echo", "hello"]
    mock_popen_init.assert_called_once()
    args, kwargs = mock_popen_init.call_args
    assert "env" in kwargs
    assert isinstance(kwargs["env"], dict)


@patch("psenv.core.command.Popen.__init__", return_value=None)
def test_command_init_env_custom(mock_popen_init):
    cmd = ["echo", "hello"]
    env = {"FOO": "BAR"}
    c = Command(cmd, env=env)
    assert c.env == env
    mock_popen_init.assert_called_once()
    args, kwargs = mock_popen_init.call_args
    assert kwargs["env"] == env


@patch("psenv.core.command.Popen.__exit__", return_value=None)
def test_command_context_manager_exit_success(mock_exit):
    c = Command(["echo", "hi"])
    c.stderr = MagicMock()
    c.stderr.read.return_value = ""
    c.wait = MagicMock(return_value=0)
    c.stderr.close = MagicMock()
    with c as ctx:
        pass
    c.stderr.close.assert_called_once()


@patch("psenv.core.command.Popen.__exit__", return_value=None)
def test_command_context_manager_exit_failure(mock_exit):
    c = Command(["echo", "hi"])
    c.stderr = MagicMock()
    c.stderr.read.return_value = "error!"
    c.wait = MagicMock(return_value=1)
    c.stderr.close = MagicMock()
    with pytest.raises(RuntimeError) as excinfo:
        with c:
            pass
    assert "Command failed with code 1" in str(excinfo.value)
    c.stderr.close.assert_called_once()
