from typing import Optional

import typer

from get50.utils import (
    _execute_shell_list,
    check_updates,
    environment,
    get_cs50_slug,
    load,
    out,
    processes,
    show,
    validate,
)

app = typer.Typer(rich_markup_mode="rich")


def run() -> None:
    # Main entry point, if anything fails show Typer error, fallback to out()
    check_updates()
    try:
        app()
    except (typer.Exit, SystemExit):
        pass
    except Exception as e:
        out(str(e), type="ERROR")


@app.command()
def check(problem: str) -> None:
    data = load()
    slug = get_cs50_slug(problem, data)

    out(f"Running check50 for [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"check50 {slug}"])


@app.command()
def submit(problem: str) -> None:
    data = load()
    slug = get_cs50_slug(problem, data)

    out(f"Submitting [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"submit50 {slug}"])


@app.command()
def download(
    problem: str = typer.Argument(help="Problem set name"),
    year: Optional[str] = typer.Option(None, "--year", "-y", help="Academic year"),
    check: Optional[str] = typer.Option(None, "--check", "-c", help="Check problem"),
    submit: Optional[str] = typer.Option(None, "--submit", "-s", help="Submit problem"),
    dry_run: bool = typer.Option(False, "--dry-run", help=""),
) -> None:
    """
    Downloads and extracts distribution code for a specific CS50 course problem.

    This command validates the requested course structure against the local data registry,
    verifies the local environment to prevent overwriting, and executes the system
    processes (wget, unzip) required to set up the problem directory.

    Args:
        problem (str): The name of the problem set or project to download.
        year (Optional[str]): The academic year. Defaults to the course's default year in data.json.
    """
    # Validate and get full metadata
    data = load()
    meta = validate(problem, year, data=data)

    # Check local environment
    environment(problem)

    # Run subprocesses
    processes(meta, dry_run=dry_run)

    # Show result
    show(problem)


if __name__ == "__main__":
    run()
