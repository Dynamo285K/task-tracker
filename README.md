# Task Tracker CLI

A simple Command Line Interface (CLI) tool for tracking and managing tasks, written in pure Python without using any external libraries. All tasks are stored locally in `~/.task-cli.json`.

## Features
*   Adding new tasks.
*   Updating the description of existing tasks.
*   Changing the status of a task (`todo`, `in-progress`, `done`).
*   Deleting tasks.
*   Listing all tasks or filtering them by their current status.
*   Automatic tracking of creation time (`createdAt`) and last update time (`updatedAt`).

## Requirements
*   **Python 3.x** (The tool uses only standard built-in modules, so there is no need to install any packages via `pip`).

## Installation
1. Download the repository or copy the script file (e.g., `task-cli.py`) to your computer.
2. Run it from anywhere, for example `python task-cli.py -l`.
3. On the first run, the script automatically creates `~/.task-cli.json` in your home directory to store data. Tasks are shared no matter which directory you run the script from.

Optional: make it executable and use it like a regular command.
```bash
chmod +x task-cli.py
./task-cli.py -l
```

## Usage

### Adding a Task
Adds a new task. The default status is `todo`.
```bash
python task-cli.py -a "Buy groceries"
```

### Listing Tasks
Lists tasks. Without an argument, all tasks are shown. You can filter by status.
```bash
# List all tasks
python task-cli.py -l

# List only tasks with a given status
python task-cli.py -l todo
python task-cli.py -l in-progress
python task-cli.py -l done
```

### Updating a Task
Updates the description of the task with the given ID.
```bash
python task-cli.py -u 1 "Buy groceries and cook dinner"
```

### Deleting a Task
Deletes the task with the given ID.
```bash
python task-cli.py -d 1
```

### Marking a Task as In Progress
Changes the status of the task with the given ID to `in-progress`.
```bash
python task-cli.py --mark-in-progress 1
```

### Marking a Task as Done
Changes the status of the task with the given ID to `done`.
```bash
python task-cli.py --mark-done 1
```

## Options

Exactly one option must be given per run; options cannot be combined.

| Option | Argument | Description |
|--------|----------|-------------|
| `-a`, `--add` | `"description"` | Add a new task |
| `-l`, `--list` | `[status]` (optional) | List tasks (`all`, `todo`, `in-progress`, `done`) |
| `-u`, `--update` | `ID "description"` | Update the description of a task |
| `-d`, `--delete` | `ID` | Delete a task |
| `--mark-in-progress` | `ID` | Set task status to `in-progress` |
| `--mark-done` | `ID` | Set task status to `done` |
| `-h`, `--help` | | Show help |

## Exit Codes and Errors

Errors are printed to `stderr`, so the tool can be safely used in scripts and pipelines.

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (task ID not found, empty description, corrupted data file) |
| `2` | Invalid arguments (unknown option, invalid status, no option given) |

```bash
python task-cli.py -d 999 && echo "deleted"   # "deleted" is not printed, exit code is 1
```