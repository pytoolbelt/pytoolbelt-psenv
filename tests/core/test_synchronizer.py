from unittest.mock import MagicMock

import pytest

from psenv.core.synchronizer import Synchronizer
from psenv.error_handling.exceptions import PsenvCLIError


class DummyCtx:
    def __init__(self):
        self.ps_client = MagicMock()


class DummyParamDiff:
    def __init__(self, to_add=None, to_update=None, to_remove=None):
        self.to_add = to_add or {}
        self.to_update = to_update or {}
        self.to_remove = to_remove or {}


def make_sync(add=None, update=None, remove=None, mode="add", dry_run=False):
    ctx = DummyCtx()
    param_diff = DummyParamDiff(add, update, remove)
    return Synchronizer(ctx, param_diff, mode, dry_run), ctx, param_diff


def test_sync_add_executes_put():
    s, ctx, _ = make_sync(add={"A": "1"}, mode="add")
    s.sync()
    ctx.ps_client.put_parameters.assert_called_once_with({"A": "1"})


def test_sync_update_executes_put_and_update():
    s, ctx, _ = make_sync(add={"A": "1"}, update={"B": "2"}, mode="update")
    s.sync()
    ctx.ps_client.put_parameters.assert_any_call({"A": "1"})
    ctx.ps_client.put_parameters.assert_any_call({"B": "2"}, overwrite=True)


def test_sync_sync_executes_all():
    s, ctx, _ = make_sync(add={"A": "1"}, update={"B": "2"}, remove={"C": "3"}, mode="sync")
    s.sync()
    ctx.ps_client.put_parameters.assert_any_call({"A": "1"})
    ctx.ps_client.put_parameters.assert_any_call({"B": "2"}, overwrite=True)
    ctx.ps_client.delete_parameters.assert_called_once_with({"C": "3"})


def test_sync_dry_run_logs(monkeypatch):
    s, ctx, _ = make_sync(add={"A": "1"}, update={"B": "2"}, remove={"C": "3"}, mode="sync", dry_run=True)
    logs = []
    monkeypatch.setattr(s.logger, "info", lambda msg, *a, **k: logs.append(msg))
    s.sync()
    assert any("Would add parameters" in m for m in logs)
    assert any("Would update parameters" in m for m in logs)
    assert any("Would remove parameters" in m for m in logs)


def test_sync_nothing_to_do(monkeypatch):
    s, ctx, _ = make_sync()
    logs = []
    monkeypatch.setattr(s.logger, "info", lambda msg, *a, **k: logs.append(msg))
    s.sync()
    assert any("No parameters to add, update, or remove" in m for m in logs)
    ctx.ps_client.put_parameters.assert_not_called()
    ctx.ps_client.delete_parameters.assert_not_called()


def test_invalid_mode_raises():
    # Provide a valid diff so sync does not return early
    s, ctx, _ = make_sync(add={"A": "1"}, mode="badmode")
    with pytest.raises(PsenvCLIError):
        s.sync()


def test_get_mode_from_flags_valid():
    assert Synchronizer.get_mode_from_flags(True, False, False) == "add"
    assert Synchronizer.get_mode_from_flags(False, True, False) == "update"
    assert Synchronizer.get_mode_from_flags(False, False, True) == "sync"


def test_get_mode_from_flags_invalid():
    with pytest.raises(ValueError):
        Synchronizer.get_mode_from_flags(False, False, False)
    with pytest.raises(ValueError):
        Synchronizer.get_mode_from_flags(True, True, False)
    with pytest.raises(ValueError):
        Synchronizer.get_mode_from_flags(True, False, True)
