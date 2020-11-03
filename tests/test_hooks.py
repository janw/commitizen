import pytest

from commitizen import hooks
from commitizen.exceptions import RunHookError


@pytest.mark.parametrize(
    "command,expected",
    [
        ("echo hello world", "hello world"),
        ("sh -c 'echo hi from subshell'", "hi from subshell"),
        (["python -c 'print(\"hello python\")'"], "hello python"),
    ],
)
def test_hooks_func(command, expected, capsys):
    hooks.run(command)
    out, _ = capsys.readouterr()
    assert "Running hook" in out
    assert expected in out


@pytest.mark.parametrize(
    "command,expected",
    [
        ("/nonexistent_command", "/nonexistent_command: No such file or directory"),
        ("python -c 'invalid python'", "SyntaxError: invalid syntax"),
    ],
)
def test_hooks_command_failure(command, expected, capsys):
    with pytest.raises(RunHookError):
        hooks.run(command)
    out, err = capsys.readouterr()
    assert "Running hook" in out
    assert expected in err


def test_hooks_environment_variable_str(capsys):
    command = 'echo "this prints $CZ_DUMMY_VAR"'
    hooks.run(command, dummy_var="a_var_value")
    out, _ = capsys.readouterr()
    out = out.splitlines()
    assert "Running hook" in out[0]
    assert "this prints $CZ_DUMMY_VAR" in out[0]
    assert "a_var_value" in out[1]


def test_hooks_environment_variable_empty(capsys):
    command = 'echo "$CZ_DUMMY_VAR"'
    hooks.run(command, dummy_var=None)
    out, _ = capsys.readouterr()
    out = out.splitlines()
    assert "Running hook" in out[0]
    assert 'echo "$CZ_DUMMY_VAR"' in out[0]
    assert len(out[1].strip()) == 0


def test_hooks_environment_variable_int(capsys):
    command = 'echo "this prints $CZ_DUMMY_VAR"'
    hooks.run(command, dummy_var=123)
    out, _ = capsys.readouterr()
    assert "123" in out


@pytest.mark.parametrize(
    "value,expected",
    [
        (True, "True"),
        (False, "False"),
    ],
)
def test_hooks_environment_variable_bool(value, expected, capsys):
    command = 'echo "$CZ_DUMMY_VAR"'
    hooks.run(command, dummy_var=value)
    out, _ = capsys.readouterr()
    assert expected in out
