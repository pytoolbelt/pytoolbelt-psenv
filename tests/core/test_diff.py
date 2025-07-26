import pytest
from psenv.core.diff import diff_parameters, ParameterDiff

@pytest.mark.parametrize("local,remote,expected_add,expected_update,expected_remove", [
    # No changes
    ({"a": "1"}, {"a": "1"}, {}, {}, {}),
    # Add parameter
    ({"a": "1", "b": "2"}, {"a": "1"}, {"b": "2"}, {}, {}),
    # Update parameter
    ({"a": "2"}, {"a": "1"}, {}, {"a": "2"}, {}),
    # Remove parameter
    ({"a": "1"}, {"a": "1", "b": "2"}, {}, {}, {"b": "2"}),
    # Add, update, and remove
    ({"a": "1", "b": "2"}, {"a": "2", "c": "3"}, {"b": "2"}, {"a": "1"}, {"c": "3"}),
    # Empty local, all remote removed
    ({}, {"a": "1", "b": "2"}, {}, {}, {"a": "1", "b": "2"}),
    # Empty remote, all local added
    ({"a": "1", "b": "2"}, {}, {"a": "1", "b": "2"}, {}, {}),
])
def test_diff_parameters(local, remote, expected_add, expected_update, expected_remove):
    diff = diff_parameters(local, remote)
    assert isinstance(diff, ParameterDiff)
    assert diff.to_add == expected_add
    assert diff.to_update == expected_update
    assert diff.to_remove == expected_remove

def test_diff_parameters_types():
    local = {"a": "1"}
    remote = {"a": "2", "b": "3"}
    diff = diff_parameters(local, remote)
    assert isinstance(diff.to_add, dict)
    assert isinstance(diff.to_update, dict)
    assert isinstance(diff.to_remove, dict)

