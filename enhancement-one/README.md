# Enhancement One: Software Engineering
CS-499 
Nicolas Valles

Original Artifact: CS-300 Project Two (C++)
Enhanced Artifact: Python CLI tool conversion

## Overview

This enhancement ports the original C++ course planner into a Python command line interface (CLI) tool. The project demonstrates modern software engineering practices by adding a modular architecture, configuration management, and type safe code design.

## Features/Additions

- CLI via `argparse` subcommands

- Persistent data cache between runs

- Config file support (config.ini)

- Type hints for readability and predictability

- Docstrings for comprehension

- Cross platform (macOS, Windows, Linux)

- Modular, maintainable

## Installation

### Dependencies

- Python 3.8 or higher
- No external dependencies (Python standard library)

### Setup

```bash
# Clone or download repository zip
cd enhancement-one

# Create venv
python -m venv venv

# Activate venv 
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Verify functionality
python -m src --help
```

## Usage 

## Quickstart commands

```bash
# Load course data from CSV (uses default from config.ini)
# Must be done first
python -m src load

# Load from specific file
python -m src load --file path/to/courses.csv

# List all courses in alphabetical order
python -m src list

# Search for specific course
python -m src search CS101

# Clear cached data
python -m src clear
```

### Verbose mode

Add `--verbose` or `-v` flag to commands for datailed output

```bash
python -m src load --verbose
python -m src list -v
```

### Help command

Information about the program or any command:

```bash
# General help
python -m src --help

# Command-specific help
python -m src load --help
python -m src list --help
python -m src search --help
```

## Project Structure
```
enhancement-one                                 # Enhancement one root directory
├── config.ini                                  # Application configuration file
├── data                                        # Directory that holds the CSV files
│   └── CS_300_ABCU_Advising_Program_Input.csv
├── README.md                                   # You are here
├── requirements.txt                            # Dependencies (empty)
└── src                                         # Project code directory
    ├── __init__.py                             # Package initialization
    ├── __main__.py                             # Module entry point
    ├── cli.py                                  # ClI interface with argparse
    ├── config_manager.py                       # Course logic
    ├── course_planner.py                       # Config management
    └── models.py                               # Course dataclass
```
## Config 

Not many features currently, but mainly to edit default path and store technical details

Edit `config.ini` file to change these settings:

```ini
[files]
default_csv_path = data/CS_300_ABCU_Advising_Program_Input.csv

[app]
name = Course Planner
version = 1.0
```

## Cache

Data persistence is achieved via `pickle` module. The cache file (`.course_cache.pkl`) was needed so data can persist between command runs without reloading the CSV each time

To force a fresh load or clear cached data:

```bash
python -m src clear
python -m src load
```

## CSV File Format

Expected CSV format:

```
CourseNumber,CourseName,Prerequisite1,Prerequisite2,...
CS101,Introduction to Computer Science
CS102,Data Structures,CS101
CS103,Algorithms,CS102
```

- First column: Course number (e.g., CS101)

- Second column: Course name

- Remaining columns: Prerequisites (optional)

## Platform Compatibility

### macOS/Linux
```bash
python3 -m src load
source venv/bin/activate
```

### Windows
```bash
python -m src load
venv\Scripts\activate
```

Uses `pathlib` for cross-platform path handling and Python standard library only

## Potential Errors

### "command not found: python"
Some platforms use the `python3` command instead, a venv should be used to mitigate this 

### "No module named src"
Make sure you're running from the `enhancement-one/` directory

### "No courses loaded"
Must run `python -m src load` first to load data and access other functionality

### "Permission denied"
Check file permissions on the data directory and CSV file

### Cache/other issues
Clear cache with `python -m src clear` and reload data