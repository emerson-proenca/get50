import difflib
import json
import os
import subprocess
import time
import urllib.request
from importlib.metadata import version
from pathlib import Path
from typing import Literal

import typer
from rich.console import Console
from rich.panel import Panel

console = Console()


def validate(
    problem: str,
    year: str | None,
    data: dict,
) -> dict:
    problem_node = resolve(problem, data, "Problem")
    selected_year = year or problem_node.get("d")
    year_data = resolve(selected_year, problem_node, "Year", context=problem)

    return {
        "problem": problem,
        "year": selected_year,
        "commands": year_data["c"],
        "slug": year_data["e"],
    }


def environment(problem: str) -> None:
    if os.path.exists(problem):
        out(f"Directory [bold red]{problem}[/bold red] already exists...", type="ERROR")
        raise typer.Exit(code=1)


def processes(meta: dict, dry_run: bool = False) -> None:
    commands = meta["commands"]

    # Case A: "c" is a String (get/unzip/rm)
    if isinstance(commands, str):
        url = f"https://cdn.cs50.net/{commands}"
        filename = url.split("/")[-1]
        cmds = [f"wget {url}", f"unzip {filename}", f"rm {filename}"]
    else:
        cmds = commands

    if dry_run:
        out(
            "[bold]Dry Run:[/bold] The following commands WOULD be executed:",
            type="WARNING",
        )
        for cmd in cmds:
            out(f"  [bold cyan]>[/bold cyan] {cmd}", type="WARNING")
        return

    _execute_shell_list(cmds)


def _execute_shell_list(commands: list[str]) -> None:
    for cmd in commands:
        try:
            # Handle 'cd' manually because subprocess.run happens in a subshell
            if cmd.startswith("cd "):
                path = cmd.replace("cd ", "").strip()
                os.chdir(path)
                continue

            # Execute the raw command
            subprocess.run(cmd, shell=True, check=True)

        except subprocess.CalledProcessError:
            out(f"Failed to execute command: {cmd}", type="ERROR")
            raise typer.Exit(1)
        except FileNotFoundError as e:
            out(f"Path not found: {e}", type="ERROR")
            raise typer.Exit(1)


def show(problem: str) -> None:
    # Simulate 'cd folder' and 'ls'
    if os.path.exists(problem):
        items = os.listdir(problem)
        console.print(f"Contents of {problem}: {items}")

    out(
        message=f"Everything setup!\nRun: [bold cyan]cd {problem}[/bold cyan]",
        type="SUCCESS",
    )


def out(message: str, type: Literal["SUCCESS", "WARNING", "ERROR"] = "SUCCESS") -> None:
    # Configuration mapping for styles
    config: dict[str, dict[str, str]] = {
        "SUCCESS": {"color": "green", "title": "Success"},
        "WARNING": {"color": "yellow", "title": "Warning"},
        "ERROR": {"color": "red", "title": "Error"},
    }

    # Retrieve style based on type (fallback to success)
    style = config.get(type.upper(), config["SUCCESS"])
    color = style["color"]
    title = style["title"]

    # Render the panel
    console.print(
        Panel(
            renderable=message,
            title=f"[bold]{title}[/bold]",
            title_align="left",
            border_style=color,
            expand=False,
            padding=(0, 1),
        )
    )


def suggest(typo: str, possibilities: list[str]) -> str:
    # Returns a 'Perhaps you meant' string if a close match is found.
    N = 1
    CUTOFF = 0.6
    matches = difflib.get_close_matches(typo, possibilities, n=N, cutoff=CUTOFF)

    if matches:
        return f"\nPerhaps you meant [bold cyan]'{matches[0]}'[/bold cyan] instead of '{typo}'?"
    return ""


def resolve(key: str, target: dict, label: str, context: str = ""):
    if key in target:
        return target[key]

    # Suggester handles the fuzzy matching
    possibilities = list(target.keys())
    suggestion = suggest(key, possibilities)

    ctx_msg = f" for '{context}'" if context else ""
    out(
        f"{label} [bold red]'{key}'[/bold red] not found{ctx_msg}.{suggestion}",
        type="ERROR",
    )
    raise typer.Exit(1)


def check_updates() -> None:
    PACKAGE_NAME = "get50"
    BASE_DIR = Path(__file__).resolve().parent
    LOCAL_DATA = BASE_DIR / "data.json"
    CACHE_FILE = Path.home() / ".get50_update_check"

    DATA_URL = (
        "https://raw.githubusercontent.com/YOUR_USER/get50/main/src/get50/data.json"
    )
    PYPI_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
    ONE_DAY = 24 * 60 * 60
    TIMEOUT = 3

    # Skip if checked recently
    if CACHE_FILE.exists() and (time.time() - CACHE_FILE.stat().st_mtime) < ONE_DAY:
        return

    try:
        # Silent Data Update (GitHub)
        with urllib.request.urlopen(DATA_URL, timeout=TIMEOUT) as response:
            new_data = json.loads(response.read().decode())
            with open(LOCAL_DATA, "w") as f:
                json.dump(new_data, f)

        # Loud Pip Update (PyPI)
        current_version = version(PACKAGE_NAME)
        with urllib.request.urlopen(PYPI_URL, timeout=TIMEOUT) as response:
            pypi_data = json.load(response)
            latest_version = pypi_data["info"]["version"]

        if latest_version != current_version:
            out(
                f"New version available: [bold]{latest_version}[/bold] (You have {current_version})\n"
                f"Run [bold cyan]pip install -U {PACKAGE_NAME}[/bold cyan] to update logic.",
                type="WARNING",
            )
        CACHE_FILE.touch()

    except Exception:
        pass


def load(file: str = "data.json") -> dict:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR / file
    if not DATA_PATH.exists():
        out(
            f"The file [bold red]{file}[/bold red] was not found at {DATA_PATH}",
            type="ERROR",
        )
        raise typer.Exit(1)

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def get_cs50_slug(problem_name: str, data: dict) -> str:
    problem_data = validate(problem_name, None, data)
    parts = problem_data["slug"].split("/")
    course = parts[0]
    year = parts[1]
    name = parts[-1]

    return f"cs50/problems/{year}/{course}/{name}"
