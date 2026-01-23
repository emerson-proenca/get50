# ez50 🚀

# CS50 made easy! Unofficial community tool and is **NOT** affiliated with Harvard University or CS50.

---

## Get Started in Seconds!

Installation and using is simple! Run this one command in your terminal:

```bash
pip install ez50
ez50 world
```

Watch the *magic* happen:

```
╭─ Success ─────────╮
│ Everything setup! │
│ Run: cd world     │
╰───────────────────╯
```

---

## What is ez50?

ez50 is a community-built tool that makes working with CS50 problem sets **EASY** (or ez!). Instead of copying and pasting commands from Harvard's website, finding the right files, and extracting them manually, you just type one command and you're ready to code!

**It's like a shortcut for everything tedious.**

---

## Commands

### 📥 Download a Problem Set
```bash
ez50 world
```

This downloads the problem set, sets up your folder, and gets everything ready to go.

### ✅ Check Your Solution
```bash
ez50 check world
# short version:
ez50 c world
```

Runs the official `check50` tool to test your code.

### 📤 Submit Your Solution
```bash
ez50 submit world
# short version:
ez50 s world
```

Submits your problem set using the official `submit50` tool.


## Nice features:
#### But I'm in a different year!
All commands support the `--year` or `-y` option:

```bash
ez50 world --year 2024
ez50 check world -y 2025
```

### 📋 Preview Without Running
Use `--dry-run` or `-dr` to see what commands will execute without actually running them:

```bash
ez50 world --dry-run
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

---

## Supported Problem Sets

**ez50** supports all* CS50 problem sets! This includes: CS50x, CS50P, CS50WEB, CS50SQL, CS50AI, CS50R

Check out the full list of supported problems in the [data.json](https://github.com/emerson-proenca/ez50/blob/main/src/ez50/data.json) file.

* We don't include CS50 for Lawyers, CS50 CyberSecurity and CS50 Scratch because you don't run those in cs50.dev (duh!)
---

## Features

✨ **One-Command Setup** — Download and extract problem sets instantly
🎯 **Smart Suggestions** — Made a typo? ez50 suggests what you probably meant:

```bash
ez50 numbers
╭─ Error ───────────────────────────────────────────╮
│ Problem 'numbers' not found.                      │
│ Perhaps you meant 'numb3rs' instead of 'numbers'? │
╰───────────────────────────────────────────────────╯
```

📅 **Multiple Years** — Access different versions of the same problem set
🔄 **Auto-Updates** — The tool checks for updates automatically
🚀 **No Hassle** — No configuration needed, just install and use

---

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

## A Note About This Tool

This is an **unofficial, community-built tool**. It is **NOT** affiliated with, endorsed by, or associated with Harvard University or the CS50 course. It's made by Students for Students to save time on repetitive tasks.

The official CS50 tools (check50, submit50) are still used under the hood, ez50 just makes them easier to access.

---

## Contributing

Found a bug? Have an idea? Contributions are welcome!

Check out the project on GitHub: [emerson-proenca/ez50](https://github.com/emerson-proenca/ez50)

If you find this tool helpful, please consider giving it a star! ⭐

---

## License

MIT License - See the repository for details.

---

**Happy coding! 💻**