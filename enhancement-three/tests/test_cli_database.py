# CS-499 Nick Valles
# Enhancement 3 - Module 5

"""
test CLI integration with database

"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd: list) -> tuple:
    """
    run a CLI command and return output
    
    Returns:
        (returncode, stdout, stderr)
    
    """
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.returncode, result.stdout, result.stderr

def test_migrate():
    """ test migrating CSV to database """

    print("=" * 70)
    print("TEST: Migrate CSV -> SQLite")
    print("=" * 70)
    
    code, out, err = run_command([
        'python3', '-m', 'src', 'migrate', '-v'
    ])
    
    print(out)
    
    if code == 0 and "MIGRATION SUCCESSFUL" in out:
        print("Migration test PASSED")
        return True
    else:
        print("Migration test FAILED")
        print(f"Error: {err}")
        return False

def test_load_database():
    """ test loading from database """

    print("=" * 70)
    print("TEST: Load from Database")
    print("=" * 70)
    
    code, out, err = run_command([
        'python3', '-m', 'src', 'load', '--database', '-v'
    ])
    
    print(out)
    
    if code == 0 and "Successfully loaded" in out:
        print("Load from database test PASSED")
        return True
    else:
        print("Load from database test FAILED")
        print(f"Error: {err}")
        return False

def test_search_database():
    """ test searching in database mode """

    print("=" * 70)
    print("TEST: Search with Database")
    print("=" * 70)
    
    # first load
    run_command(['python3', '-m', 'src', 'load', '--database'])
    
    # search after
    code, out, err = run_command([
        'python3', '-m', 'src', 'search', 'CSCI101', '-v'
    ])
    
    print(out)
    
    if code == 0 and ("CSCI101" in out or "parameterized SQL query" in out):
        print("Search with database test PASSED")
        return True
    else:
        print("Search with database test FAILED")
        print(f"Error: {err}")
        return False

def test_list_database():
    """ test listing courses from database """
    print("=" * 70)
    print("TEST: List with Database")
    print("=" * 70)
    
    # load first
    run_command(['python3', '-m', 'src', 'load', '--database'])
    
    # then list
    code, out, err = run_command([
        'python3', '-m', 'src', 'list', '-v'
    ])
    
    print(out)
    
    if code == 0 and "sample schedule" in out:
        print("List with database test PASSED")
        return True
    else:
        print("List with database test FAILED")
        print(f"Error: {err}")
        return False

def test_validate_database():
    """ test validation with database """
    print("=" * 70)
    print("TEST: Validate with Database")
    print("=" * 70)
    
    # Load first
    run_command(['python3', '-m', 'src', 'load', '--database'])
    
    # Then validate
    code, out, err = run_command([
        'python3', '-m', 'src', 'validate', '-v'
    ])
    
    print(out)
    
    if code == 0 and "verified as valid" in out:
        print("Validate with database test PASSED")
        return True
    else:
        print("Validate with database test FAILED")
        print(f"Error: {err}")
        return False

def test_csv_mode_still_works():
    """ test that CSV mode still works """
    print("=" * 70)
    print("TEST: CSV Mode (Backward Compatibility)")
    print("=" * 70)
    
    # clear cache first
    run_command(['python3', '-m', 'src', 'clear'])
    
    # load CSV (no --database flag)
    code, out, err = run_command([
        'python3', '-m', 'src', 'load', '-v'
    ])
    
    print(out)
    
    if code == 0 and "Successfully loaded" in out:
        print("CSV mode test PASSED")
        return True
    else:
        print("CSV mode test FAILED")
        print(f"Error: {err}")
        return False

def cleanup():
    """ remove test database"""
    db_file = Path(__file__).parent.parent / 'course_catalog.db'
    if db_file.exists():
        db_file.unlink()
        print("\n🧹 Cleaned up test database")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CLI DATABASE INTEGRATION TESTS")
    print("=" * 70)
    print()
    
    try:
        tests = [
            test_migrate(),
            test_load_database(),
            test_search_database(),
            test_list_database(),
            test_validate_database(),
            test_csv_mode_still_works()
        ]
        
        print("\n" + "=" * 70)
        if all(tests):
            print("ALL CLI DATABASE TESTS PASSED")
        else:
            passed = sum(tests)
            total = len(tests)
            print(f"⚠ {passed}/{total} tests passed")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()