import difflib
import json
import os
import subprocess
import time
import urllib.request
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Literal

import typer
from rich.console import Console
from rich.panel import Panel

console = Console()


def validate(
    course: str,
    week: str,
    problem: str,
    year: str | None,
    season: str | None,
    p_type: str | None,
    format: str | None,
    data: dict,
) -> dict[str, str]:
    # Resolve Course (Root Level)
    course_id = course.lower()
    course_node = resolve(course_id, data, "Course")

    # Resolve Defaults
    res_year = year or course_node["default"]["year"]
    res_season = season or course_node["default"]["season"]
    res_type = p_type or course_node["default"]["type"]
    res_format = format or course_node["default"]["format"]

    # Walk the Tree (Year -> Season -> Type)
    year_node = resolve(res_year, course_node, "Year", context=course_id)
    season_node = resolve(
        res_season, year_node, "Season", context=f"{course_id} {res_year}"
    )
    type_node = resolve(
        res_type, season_node, "Type", context=f"{course_id} {res_year} {res_season}"
    )

    # Final Leaf Check (Week & Problem)
    if res_type == "psets":
        problem_list = resolve(
            week, type_node, "Week", context=f"{res_type} {res_year}"
        )
    else:
        # Projects are usually a direct list
        problem_list = type_node

    # Problem check (Searching in a list, not a dict)
    if problem not in problem_list:
        suggestion = suggest(problem, problem_list)
        out(f"Problem '{problem}' not found.{suggestion}", type="ERROR")
        raise typer.Exit(1)

    return {
        "course": course_id,
        "year": res_year,
        "season": res_season,
        "type": res_type,
        "week": week,
        "problem": problem,
        "format": res_format,
    }


def environment(problem: str) -> None:
    if os.path.exists(problem):
        out(f"Directory [bold red]{problem}[/bold red] already exists...", type="ERROR")
        raise typer.Exit(code=1)


def processes(meta: dict[str, str]) -> None:
    BASE_URL = "https://cdn.cs50.net"
    week_part = f"/{meta['week']}" if meta["type"] == "psets" else ""

    url = f"{BASE_URL}/{meta['course']}/{meta['year']}/{meta['season']}/{meta['type']}{week_part}/{meta['problem']}{meta['format']}"
    zip_file = f"{meta['problem']}{meta['format']}"

    try:
        subprocess.run(["wget", url], check=True)
        subprocess.run(["unzip", zip_file], check=True)
        subprocess.run(["rm", zip_file], check=True)

    except subprocess.CalledProcessError:
        out(
            "Failed to download or extract distribution code.",
            type="ERROR",
        )
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

    # Generate suggestion from the available keys in this specific level
    possibilities = list(target.keys())
    suggestion = suggest(key, possibilities)

    location = f" in {context}" if context else ""
    out(f"{label} '{key}' not found{location}.{suggestion}", type="ERROR")
    raise typer.Exit(1)


def check_updates():
    # Checks PyPI for a newer version once every 24 hours
    PACKAGE_NAME = "get50"
    CACHE_FILE = Path.home() / ".get50_update_check"
    ONE_DAY = 24 * 60 * 60

    if CACHE_FILE.exists():
        last_check = CACHE_FILE.stat().st_mtime
        if (time.time() - last_check) < ONE_DAY:
            return

    try:
        current_version = version(PACKAGE_NAME)

        # Fetch latest version from PyPI
        TIMEOUT = 3
        url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            data = json.load(response)
            latest_version = data["info"]["version"]

        # Compare and notify
        if latest_version != current_version:
            out(
                f"New version available: [bold]{latest_version}[/bold] (You have {current_version})\nRun [bold cyan]pip install -U {PACKAGE_NAME}[/bold cyan] to update.",
                type="WARNING",
            )

        # Update cache timestamp even if no update is found
        CACHE_FILE.touch()

    except (PackageNotFoundError, Exception):
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
