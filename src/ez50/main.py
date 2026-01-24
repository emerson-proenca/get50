import sys
from typing import Optional

import typer

from ez50.commands import check, download, submit
from ez50.options import version_callback
from ez50.utils import check_updates, out

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
)

COMMANDS = {"check", "c", "submit", "s", "download"}


def run() -> None:
    check_updates()
    args = sys.argv[1:]

    if args and args[0] not in COMMANDS and not args[0].startswith("-"):
        args.insert(0, "download")

    try:
        app(args=args)
    except (typer.Exit, SystemExit):
        pass
    except Exception as e:
        out(str(e), type="ERROR")


@app.callback()
def options(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """
    [bold cyan]CS50 made easy![/bold cyan]

    Unofficial community tool and is NOT affiliated with Harvard University or CS50.
    """
    pass


app.command(name="download")(download)
app.command(name="check")(check)
app.command(name="submit")(submit)
app.command(name="c", hidden=True)(check)
app.command(name="s", hidden=True)(submit)

if __name__ == "__main__":
    run()
