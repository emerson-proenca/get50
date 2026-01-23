# ez50 (CS50 made easy!)

> Unofficial community tool and is **NOT** affiliated with Harvard University or CS50.

## Get Started in Seconds!

Installation and use is simple! Just run in your terminal:

```bash
pip install ez50
ez50 world
```

Watch the _magic_ happen:

<div class="termy">

```console
╭─ Success ─────────╮
│ Everything setup! │
│ Run: cd world     │
╰───────────────────╯
```

</div>

---

## What is ez50?

**ez50** is a community tool that makes working with CS50 problem sets **EASY** (or ez). Instead of copying and pasting commands from harvard.edu, finding the right files, and extracting them manually, you just type one command and you're ready!

### Key features:

- **One-Command Setup**: Download and extract problem sets instantly
- **Smart Suggestions**: Made a typo? **ez50** suggests what you probably meant
- **Multiple Years**: Access different versions of the same problem set
- **Auto-Updates**: The tool checks for updates automatically
- **No Hassle**: No configuration needed, just install and use

## Commands

### Download a Problem Set

```bash
ez50 world
```

This downloads the problem set, sets up your folder, and gets everything ready to go!

### Check Your Solution

```bash
$ ez50 check world
# short version:
$ ez50 c world
```

Runs the official `check50` tool to test your code.

### Submit Your Solution

```bash
ez50 submit world
# short version:
ez50 s world
```

Submits your problem set using the official `submit50` tool.

## Nice Features:

### I'm in a different year!

All commands support the `--year` or `-y` option:

```bash
ez50 world --year 2024
ez50 check world -y 2025
```

### I don't trust you!

Use `--dry-run` or `-dr` to see what commands WOULD execute, without actually **executing** them:

<div class="termy">

```console
$ ez50 world --dry-run
╭─ Info ─────────────────────────────────────────────╮
│ Dry Run: The following commands WOULD be executed: │
╰────────────────────────────────────────────────────╯
╭─ Info ───────────╮
│   > mkdir world  │
│   > cd world     │
│   > code hello.c │
│   > ls           │
╰──────────────────╯
```

</div>

### Does it include my course?

**ez50** supports _all_ CS50 problem sets! This includes: **CS50x**, **CS50P**, **CS50WEB**, **CS50SQL**, **CS50AI** and **CS50R**

Check out the full list of supported problems in the [data.json](https://github.com/emerson-proenca/ez50/blob/main/src/ez50/data.json) file.

> _all_: We don't include CS50: Law, CyberSecurity and Scratch. Because those don't have problem sets.

### What else?

**ez50** magically suggests what you _probably_ meant:

<div class="termy">

```console
$ ez50 numbers
╭─ Error ───────────────────────────────────────────╮
│ Problem 'numbers' not found.                      │
│ Perhaps you meant 'numb3rs' instead of 'numbers'? │
╰───────────────────────────────────────────────────╯
```

</div>

## Installation Troubleshooting

**Problem: `pip: command not found`**

You might not have Python installed. Download it from [python.org](https://www.python.org/downloads/).

**Problem: `Permission denied`**

Try adding `--user` to the installation:

```bash
pip install --user ez50
```

**Problem: `ez50: command not found`**

Make sure the installation completed without errors. Try:

```bash
python -m pip install ez50
```

---

## About

This is an **unofficial, community-built tool**. It is **NOT** affiliated with, endorsed by, or associated with Harvard University or the CS50 course. It's made by Students for Students to save time on repetitive tasks.

The official CS50 tools (check50, submit50) are still used under the hood, **ez50** just makes them easier to use.

## Contributing

Found a bug? Have an idea? Contributions are welcome!

Check out the project on GitHub: [emerson-proenca/ez50](https://github.com/emerson-proenca/ez50)

If you find this tool helpful, please consider giving it a star! ⭐

## License

MIT License - See the [LICENSE](https://github.com/emerson-proenca/ez50?tab=MIT-1-ov-file)
