from typing import Optional

import typer

from get50.utils import check_updates, environment, load, out, processes, show, validate

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
def download(
    course: str = typer.Argument(help="Course name (e.g., sql)"),
    week: str = typer.Argument(help="Week number"),
    file: str = typer.Argument(help="Problem set name"),
    year: Optional[str] = typer.Option(None, "--year", "-y", help="Academic year"),
    season: Optional[str] = typer.Option(None, "--season", "-s", help="Course season"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Assignment type"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="File format"),
) -> None:
    """
    Downloads and extracts distribution code for a specific CS50 course problem.

    This command validates the requested course structure against the local data registry,
    verifies the local environment to prevent overwriting, and executes the system
    processes (wget, unzip) required to set up the problem directory.

    Args:
        course (str): The identifier for the course (e.g., 'sql', 'python').
        week (str): The specific week or module number of the course.
        file (str): The name of the problem set or project to download.
        year (Optional[str]): The academic year. Defaults to the course's default year in data.json.
        season (Optional[str]): The course season (e.g., 'fall', 'spring', 'x'). Defaults to course default.
        type (Optional[str]): The assignment type ('pset' or 'project'). Defaults to 'pset'.
        format (Optional[str]): The file extension to download. Defaults to '.zip'.
    """
    # Validate and get full metadata
    DATA = load()
    meta = validate(course, week, file, year, season, type, format, data=DATA)

    # Check local environment
    environment(file)

    # Run subprocesses
    processes(meta)

    # Show result
    show(file)


if __name__ == "__main__":
    run()
