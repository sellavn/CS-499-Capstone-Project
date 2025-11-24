# Enhancement Two: Algorithms

CS-499 
Nicolas Valles

Original Artifact: CS-300 Project Two (C++)
Enhanced Artifact: Python CLI tool conversion

## Overview

Enhancement Two builds upon the previous Enhancement One by implementing advanced data structures and algorithms to improve performance within the CLI application. The focus is on replacing inefficient linear search operations with hash map indexing and implementing Depth-First Search (DFS) for prerequisite validation with cycle detection. A benchmark test has also been implemented to showcase improvements.

## Features/Additions

- Hash Map Indexing
  
  - Enhancement One used linear search through vector - O(n) time complexity
  
  - Enhancement Two Improves via dictionary-based hash map - O(1) time complexity

- DFS Cycle Detection
  
  - Validates prerequisite relationships for circular dependencies
  
  - Graph traversal using Depth-First Search algorithm
  
  - Time Complexity: O(V + E) where V = courses, E = prerequisites
  
  - Prevents invalid course sequences

- Prerequisite Validation System
  
  - Checks for non-existent prerequisites
  
  - Detects circular dependency chains
  
  - Manual validation command

## Performance Improvements

Taken from `benchmark_performance.py` within the `tests` directory

```
======================================================================
PERFORMANCE BENCHMARK: Linear Search vs Hash Map Lookup
======================================================================

Dataset: 4 courses
Iterations: 1,000 searches per method

Testing linear search (O(n)):
 Total time: 0.0023 seconds
 Average per search: 0.56 microseconds

Testing hash map lookup (0(1)):
 total time: 0.0016 seconds
 Average per search: 0.41 microseconds

======================================================================
results
======================================================================
speed up factor: 1.37x faster
performance improvement: 27.0%

analysis
----------------------------------------------------------------------
Linear search O(n):
 - Checks up to 4 courses per search
 - Time grows linearly with dataset size
 - Average case: n/2 comparisons

Hash map lookup O(1):
 - Direct index access in constant time
 - Time remains constant regardless of dataset size
 - Always 1 operation

With 4 courses, hash map is ~1.4x faster
This advantage grows significantly with larger datasets

Projected Scaling
----------------------------------------------------------------------
With 40 courses:
 Linear search: ~20 comparisons on average
 Hash map:      1 operation (constant)

With 400 courses:
 Linear search: ~200 comparisons on average
 Hash map:      1 operation (constant)

With 4,000 courses:
 Linear search: ~2,000 comparisons on average
 Hash map:      1 operation (constant)

With 40,000 courses:
 Linear search: ~20,000 comparisons on average
 Hash map:      1 operation (constant)

======================================================================

======================================================================
DFS cycle detection performance
======================================================================

dataset: 4 courses
running validation with DFS cycle detection

validation completed in: 0.01 milliseconds
result: Valid
issues found: 0

complexity analysis
----------------------------------------------------------------------
DFS cycle detection: O(V + E)
 V (vertices/courses): 4
 E (edges/prerequisites): 3

DFS visits each course once then checks each prerequisite once,
making it fairly efficient for larger course catalogs
```

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

# Search for specific course (now uses hash map)
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

## Validate Command

Manually validate prerequisites and find warnings or errors

```bash 
python3 -m src validate
python3 -m src --verbose validate
```

## Performance Benchmark

**Make sure you are in the enhancement-two directory**

```bash 
python3 tests/benchmark_performance.py 
```

## Project Structure

```
enhancement-two                                # Enhancement two directory          
├── config.ini                                 # Application configuration file
├── data                                       # Directory that holds the CSV files
│   ├── CS_300_ABCU_Advising_Program_Input.csv # Standard CSV file - no errors
│   ├── test_circular.csv                      # CSV file that shows basic circular dependency errors
│   ├── test_complex_circular.csv              # CSV file that shows complex circular dependency errors
│   └── test_missing_prereq.csv                # CSV file that tests missing prerequisites
├── README.md                                  # You are here
├── requirements.txt                           # Dependencies (empty)
├── src                                        # Project code directory
│   ├── cli.py                                 # CLI interface with argparse
│   ├── config_manager.py                      # Configuration
│   ├── course_planner.py                      # Course logic and algorithms
│   ├── __init__.py                            # Package initialization
│   ├── __main__.py                            # Entry point
│   ├── models.py                              # Data models
└── tests
    └── benchmark_performance.py               # Performance benchmark

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

Make sure you're running from the `enhancement-two/` directory

### "No courses loaded"

Must run `python -m src load` first to load data and access other functionality

### "Permission denied"

Check file permissions on the data directory and CSV file

### Cache/other issues

Clear cache with `python -m src clear` and reload data