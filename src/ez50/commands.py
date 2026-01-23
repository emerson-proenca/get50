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
    [bold]Check[/bold] a solution using [bold]check50[/bold].

    [bold]Args:[/bold]
        [blue]problem[/blue]: Name or slug of the problem set.
        [blue]year[/blue]: Targeted academic year.
        [blue]dry_run[/blue]: Preview the command without running.

    [italic]Consider starring:[/italic] [link=https://github.com/emerson-proenca/ez50]https://github.com/emerson-proenca/ez50[/link]
    """
    data = load()
    slug = get_cs50_slug(problem, data, year)
    if not dry_run:
        out(f"Running check50 for [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"check50 {slug}"], dry_run)


def submit(
    problem: str,
    year: Optional[str] = typer.Option(
        None, "--year", "-y", help="Academic year to use"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-dr", help="Run without executing"
    ),
) -> None:
    """
    [bold]Submit[/bold] a solution using [bold]submit50[/bold].

    [bold]Args:[/bold]
        [blue]problem[/blue]: Name or slug of the problem set.
        [blue]year[/blue]: Targeted academic year.
        [blue]dry_run[/blue]: Preview the command without running.

    [italic]Consider starring:[/italic] [link=https://github.com/emerson-proenca/ez50]https://github.com/emerson-proenca/ez50[/link]
    """
    data = load()
    slug = get_cs50_slug(problem, data, year)

    if not dry_run:
        out(f"Submitting [bold]{problem}[/bold]...", type="WARNING")
    _execute_shell_list([f"submit50 {slug}"], dry_run)


def download(
    problem: str = typer.Argument(help="Problem set name"),
    year: Optional[str] = typer.Option(
        None, "--year", "-y", help="Academic year to use"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-dr", help="Run without executing"
    ),
) -> None:
    """
    [bold]Download[/bold] and extract a pset environment.

    [bold]Args:[/bold]
        [blue]problem[/blue]: Name of the pset to download.
        [blue]year[/blue]: Targeted academic year.
        [blue]dry_run[/blue]: Log actions without downloading.

    [italic]Consider starring:[/italic] [link=https://github.com/emerson-proenca/ez50]https://github.com/emerson-proenca/ez50[/link]
    """
    data = load()
    meta = validate(problem, year, data=data)

    environment(problem)
    processes(meta, dry_run=dry_run)
    show(problem)
