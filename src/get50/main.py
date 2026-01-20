import subprocess

import typer

app = typer.Typer()


@app.command()
def download(course: str, week: str, pset: str):
    """_summary_

    Args:
        course (str): _description_
        week (str): _description_
        pset (str): _description_

    Raises:
        typer.Exit: _description_
    """
    week_num = week.replace("week", "")
    url = f"https://cdn.cs50.net/2026/x/psets/{week_num}/{pset}.zip"
    zip_file = f"{pset}.zip"

    typer.echo(f"🚀 Fetching {pset} from {course}...")

    try:
        subprocess.run(["wget", url], check=True)
        subprocess.run(["unzip", zip_file], check=True)
        subprocess.run(["rm", zip_file], check=True)

        typer.secho(
            f"✅ Success! Problem set '{pset}' is ready.", fg=typer.colors.GREEN
        )
        typer.echo(f"Type 'cd {pset}' to begin.")

    except subprocess.CalledProcessError as e:
        typer.secho(
            f"❌ Error: Could not download the problem set. error: {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
