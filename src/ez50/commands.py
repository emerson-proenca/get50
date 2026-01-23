from typing import Optional

import typer

from ez50.utils import (
    _execute_shell_list,
    environment,
    get_cs50_slug,
    load,
    out,
    processes,
    show,
    validate,
)

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="This is an unofficial community tool and is NOT affiliated with Harvard University or CS50.",
)


@app.command(name="check")
def check(
    problem: str,
    year: Optional[str] = typer.Option(
        None, "--year", "-y", help="Academic year to use"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-dr", help="Run without executing"
    ),
) -> None:
    """
    Check a problem set solution using check50. Alias for 'check'.

    Args:
        problem (str): _description_
        year (Optional[str], optional): _description_. Defaults to typer.Option( None, "--year", "-y", help="Academic year to use" ).
        dry_run (bool, optional): _description_. Defaults to typer.Option( False, "--dry-run", "-dr", help="Run without executing" ).
    """
    data = load()
    slug = get_cs50_slug(problem, data, year)
    if not dry_run:
        out(f"Running check50 for [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"check50 {slug}"], dry_run=dry_run)


@app.command(name="submit")
def submit(
    problem: str,
    year: Optional[str] = typer.Option(
        None, "--year", "-y", help="Academic year to use"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-dr", help="Run without executing"
    ),
) -> None:
    """_summary_

    Args:
        problem (str): _description_
        year (Optional[str], optional): _description_. Defaults to typer.Option( None, "--year", "-y", help="Academic year to use" ).
        dry_run (bool, optional): _description_. Defaults to typer.Option( False, "--dry-run", "-dr", help="Run without executing" ).
    """
    data = load()
    slug = get_cs50_slug(problem, data, year)

    if not dry_run:
        out(f"Submitting [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"submit50 {slug}"], dry_run=dry_run)


@app.command()
def download(
    problem: str = typer.Argument(help="Problem set name"),
    year: Optional[str] = typer.Option(
        None, "--year", "-y", help="Academic year to use"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-dr", help="Run without executing"
    ),
) -> None:
    """_summary_

    Args:
        problem (str, optional): _description_. Defaults to typer.Argument(help="Problem set name").
        year (Optional[str], optional): _description_. Defaults to typer.Option( None, "--year", "-y", help="Academic year to use" ).
        dry_run (bool, optional): _description_. Defaults to typer.Option( False, "--dry-run", "-dr", help="Run without executing" ).
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
