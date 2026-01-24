from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from ez50.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_utils():
    """Mock external utilities to prevent side effects during testing."""
    with (
        patch("ez50.main.check_updates"),
        patch("ez50.commands.load") as mock_load,
        patch("ez50.commands.validate"),
        patch("ez50.commands.get_cs50_slug") as mock_slug,
        patch("ez50.commands._execute_shell_list"),
        patch("ez50.commands.environment"),
        patch("ez50.commands.processes"),
        patch("ez50.commands.show"),
        patch("ez50.options.metadata.version") as mock_ver,
    ):
        mock_load.return_value = {}
        mock_slug.return_value = "competitions/2023/hello"
        mock_ver.return_value = "1.0.0"
        yield


# --- Option Tests ---


@pytest.mark.parametrize("option", ["--help", "--version", "-v"])
def test_options(option):
    """Tests standard CLI options."""
    result = runner.invoke(app, [option])
    assert result.exit_code == 0
    if "version" in option or option == "-v":
        assert "ez50 version 1.0.0" in result.stdout


def test_no_args_shows_help():
    """Tests that running without args shows help."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


# --- Command Tests ---


@pytest.mark.parametrize(
    "args",
    [
        ["hello"],
        ["download", "hello"],
        ["check", "hello"],
        ["submit", "hello"],
        ["s", "hello"],
        ["c", "hello"],
        ["hello", "--year", "2023"],
        ["c", "hello", "--year", "2023"],
        ["s", "hello", "--year", "2023"],
        ["hello", "-y", "2023"],
        ["c", "hello", "-y", "2023"],
        ["s", "hello", "-y", "2023"],
        ["hello", "--dry-run"],
        ["c", "hello", "--dry-run"],
        ["s", "hello", "--dry-run"],
        ["hello", "-dr"],
        ["c", "hello", "-dr"],
        ["s", "hello", "-dr"],
        ["hello", "-dr", "-y", "2023"],
        ["c", "hello", "-dr", "-y", "2023"],
        ["s", "hello", "-dr", "-y", "2023"],
    ],
)
def test_correct_usage(args):
    """Tests all valid command combinations and aliases."""
    result = runner.invoke(app, args)
    assert result.exit_code == 0


# --- Error and Typo Tests ---


def test_incorrect_usage():
    """Tests behavior when an invalid option is passed."""
    result = runner.invoke(app, ["check", "hello", "--invalid-flag"])
    assert result.exit_code != 0
    assert "No such option" in result.stdout


def test_typo_suggestion():
    """
    Tests for typo suggestions.
    Note: Typer/Click provides 'Did you mean' automatically for commands.
    """
    result = runner.invoke(app, ["checkk", "hello"])
    assert result.exit_code != 0
    # Typer's default error message for similar commands
    assert "No such command 'checkk'" in result.stdout
    assert "Perhaps you meant 'check'?" in result.stdout
