from importlib import metadata

import typer

from ez50.utils import out


def version_callback(value: bool):
    """
    Shows the current [bold]Version[/bold] and exits.

    [italic]Consider starring:[/italic] [link=https://github.com/emerson-proenca/ez50]https://github.com/emerson-proenca/ez50[/link]
    """
    if value:
        try:
            version = metadata.version("ez50")
            out(f"ez50 version {version}")
        except metadata.PackageNotFoundError:
            out("ez50 version unknown", type="ERROR")
        raise typer.Exit()
