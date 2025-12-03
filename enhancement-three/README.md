# Enhancement Three: Databases

CS-499 
Nicolas Valles

Original Artifact: CS-300 Project Two (C++)
Enhanced Artifact: Python CLI tool conversion

## Overview

Enhancement Three adds greater functionality to the Course Planner by creating a production-ready application with SQLite database integration, parameterized queries for SQL injection prevention, and persistent data storage.

## Features/Additions

- SQLite Database Integration - Persistent storage with relational schema via SQLite

- Parameterized Queries - SQL injection prevention on all database operations

- Transaction Management - ACID compliance with automatic rollback on errors

- ETL Pipeline - CSV-to-SQLite migration with data validation

- Many-to-Many Relationships - Proper junction table for prerequisites

- Backward Compatibility - CSV mode still available for comparison

- CRUD Operations - Full Create, Read, Update, Delete support

### Tables

#### `courses` Table
Stores individual course information with unique identifiers.

| Column        | Type      | Constraints           | Description                    |
|---------------|-----------|----------------------|--------------------------------|
| course_id     | INTEGER   | PRIMARY KEY, AUTO    | Unique course identifier       |
| course_number | TEXT      | UNIQUE, NOT NULL     | Course code (e.g., CSCI101)   |
| course_name   | TEXT      | NOT NULL             | Full course name              |
| created_at    | TIMESTAMP | DEFAULT CURRENT      | Record creation timestamp     |
| updated_at    | TIMESTAMP | DEFAULT CURRENT      | Last update timestamp         |

#### `prerequisites` Junction Table
Implements many-to-many relationships between courses.

| Column                  | Type      | Constraints        | Description                        |
|------------------------|-----------|-------------------|------------------------------------|
| prerequisite_id        | INTEGER   | PRIMARY KEY, AUTO  | Unique relationship identifier     |
| course_id              | INTEGER   | FK, NOT NULL       | Course requiring prerequisite      |
| prerequisite_course_id | INTEGER   | FK, NOT NULL       | Course that is the prerequisite    |
| created_at             | TIMESTAMP | DEFAULT CURRENT    | Relationship creation timestamp    |

**Constraints:**

- Foreign key to `courses(course_id)` with CASCADE delete

- Unique constraint on `(course_id, prerequisite_course_id)` to prevent duplicates

### Performance Indexes

```sql
CREATE INDEX idx_course_number ON courses(course_number);
CREATE INDEX idx_prerequisites_course ON prerequisites(course_id);
CREATE INDEX idx_prerequisites_prereq ON prerequisites(prerequisite_course_id);
```

**Performance Impact:**

- Course lookups: O(log n) with B-tree index vs O(n) table scan

- Prerequisite queries: Indexed joins eliminate nested loops

- Typical query time: <1ms for catalogs with 1000+ courses


## Installation

### Dependencies

- Python 3.8 or higher

- No external dependencies (Python standard library)

### Setup

```bash
git clone https://github.com/sellavn/CS-499-Capstone-Project.git

cd CS-499-Capstone-Project/enhancement-three

# Verify installation
python3 -m src --version

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

### Database Mode vs CSV Mode

Enhancement Three supports **two operating modes**:

| Feature              | CSV Mode (Legacy)          | Database Mode (New)           |
|---------------------|----------------------------|-------------------------------|
| Storage             | Pickle cache file          | SQLite database file          |
| Persistence         | Session-based              | Permanent                     |
| Relationships       | In-memory only             | Foreign key constraints       |
| Concurrent Access   | Not supported              | Supported with locking        |
| Query Language      | Python (hash map)          | SQL (parameterized)           |
| Security            | N/A                        | SQL injection prevention      |


## Command Reference

**First-time setup:** Convert CSV data to SQLite database.

```bash
# Migrate with default settings
python3 -m src migrate

# Migrate with verbose output
python3 -m src migrate -v

# Migrate custom CSV file
python3 -m src migrate --file data/custom_courses.csv

# Migrate to custom database
python3 -m src migrate --db-path my_catalog.db
```

### Load Courses

**Load from database**
```bash
python3 -m src load --database
python3 -m src load --database -v                    # Verbose mode
python3 -m src load --database --db-path custom.db   # Custom database
```

**Load from CSV**
```bash
python3 -m src load
python3 -m src load --file data/custom.csv
```

### Search for Course

```bash
# Database mode (must load with --database first)
python3 -m src load --database
python3 -m src search CSCI101
python3 -m src search CSCI101 -v    # Shows "Using parameterized SQL query"

# CSV mode
python3 -m src load
python3 -m src search CSCI101        # Uses hash map O(1) lookup
```

### List All Courses

```bash
python3 -m src list
python3 -m src list -v    # Shows data source (database vs memory)
```

### Validate Prerequisites

Checks for circular dependencies and missing prerequisites.

```bash
python3 -m src validate
python3 -m src validate -v    # Verbose output
```

### Clear Cache

```bash
python3 -m src clear    # Clears pickle cache (CSV mode only)
```

---

## Project Structure

```
enhancement-three
├── config.ini                                  # Application configuration
├── data                                        # CSV datasets, .db file created after migration
│   ├── CS_300_ABCU_Advising_Program_Input.csv
│   ├── test_circular.csv
│   ├── test_complex_circular.csv
│   └── test_missing_prereq.csv
├── README.md                                   # You are here
├── requirements.txt                            # Dependencies (empty)
├── src                                         # Source code directory
│   ├── __init__.py                             # Package initialization
│   ├── __main__.py                             # Module entry point
│   ├── cli.py                                  # Command-line interface
│   ├── config_manager.py                       # Configuration handling
│   ├── course_planner.py                       # Core logic
│   ├── database.py                             # Database manager
│   └── models.py                               # Course data model
└── tests                                       # Testing directory for benchmarks/functionality
    ├── benchmark_performance.py
    ├── test_cli_database.py
    └── test_crud.py

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

## Testing

### Test Suite

A couple of testing programs were made prior to full functionality implementation

```bash

# CRUD operations
python3 tests/test_crud.py

# CLI integration
python3 tests/test_cli_database.py
```

### Test Coverage

- CRUD operations (Create, Read, Update, Delete)

- Prerequisite management (add, remove, query)

- Transaction rollback (error handling)

- CLI commands (all 6 commands)

- Backward compatibility (CSV mode still works)

- SQL injection prevention (all queries parameterized)


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