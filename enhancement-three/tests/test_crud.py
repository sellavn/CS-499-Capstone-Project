# CS-499 Nick Valles
# Enhancement 3 - Module 5

"""
test CRUD operations for database

"""

import sys
from pathlib import Path

# add directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager

def test_create():
    """ test creating courses """

    print("=" * 70)
    print("TEST: CREATE Operations")
    print("=" * 70)
    print()
    
    db = DatabaseManager('test_crud.db', verbose=True)
    db.drop_schema()
    db.create_schema()
    
    # create courses
    id1 = db.add_course("CSCI100", "Introduction to Programming")
    id2 = db.add_course("CSCI101", "Data Structures")
    id3 = db.add_course("CSCI200", "Algorithms")
    
    if id1 and id2 and id3:
        print("\n CREATE test PASSED - 3 courses created")
    else:
        print("\n CREATE test FAILED")
        return False
    
    # try duplicate
    print("\nTesting duplicate course (should fail):")
    id_dup = db.add_course("CSCI100", "Duplicate")
    if not id_dup:
        print(" Duplicate handling works correctly")
    
    db.close()
    print()
    return True

def test_read():
    """ test reading courses """

    print("=" * 70)
    print("TEST: READ Operations")
    print("=" * 70)
    print()
    
    db = DatabaseManager('test_crud.db', verbose=True)
    
    # get single course
    course = db.get_course_by_number("CSCI101")
    if course:
        print(f"Found course: {course.course_number} - {course.name}")
    else:
        print("Failed to retrieve course")
        return False
    
    # get all courses
    courses = db.get_all_courses()
    print(f"\n Retrieved {len(courses)} courses:")
    for c in courses:
        print(f"  - {c.course_number}: {c.name}")
    
    # Get count
    count = db.get_course_count()
    print(f"\n Total course count: {count}")
    
    if len(courses) == count:
        print("\n READ test PASSED")
    else:
        print("\n READ test FAILED - count mismatch")
        return False
    
    db.close()
    print()
    return True

def test_update():
    """ test updating courses """

    print("=" * 70)
    print("TEST: UPDATE Operations")
    print("=" * 70)
    print()
    
    db = DatabaseManager('test_crud.db', verbose=True)
    
    # Update course name
    success = db.update_course("CSCI100", "Intro to Computer Science")
    
    if success:
        # Verify update
        course = db.get_course_by_number("CSCI100")
        if course and "Intro to Computer Science" in course.name:
            print("\n UPDATE test PASSED")
        else:
            print("\n UPDATE test FAILED - verification failed")
            return False
    else:
        print("\n UPDATE test FAILED")
        return False
    
    db.close()
    print()
    return True

def test_prerequisites():
    """ test prerequisite operations """

    print("=" * 70)
    print("TEST: Prerequisite Operations")
    print("=" * 70)
    print()
    
    db = DatabaseManager('test_crud.db', verbose=True)
    
    # Add prerequisites
    success1 = db.add_prerequisite("CSCI101", "CSCI100")
    success2 = db.add_prerequisite("CSCI200", "CSCI101")
    
    if not (success1 and success2):
        print("\n Failed to add prerequisites")
        return False
    
    # Get prerequisites
    prereqs_101 = db.get_prerequisites("CSCI101")
    prereqs_200 = db.get_prerequisites("CSCI200")
    
    print(f"\nCSCI101 prerequisites: {prereqs_101}")
    print(f"CSCI200 prerequisites: {prereqs_200}")
    
    if "CSCI100" in prereqs_101 and "CSCI101" in prereqs_200:
        print("\n Prerequisite test PASSED")
    else:
        print("\n Prerequisite test FAILED")
        return False
    
    # Remove prerequisite
    print("\nRemoving CSCI200 → CSCI101 prerequisite:")
    success = db.remove_prerequisite("CSCI200", "CSCI101")
    
    if success:
        prereqs_200_after = db.get_prerequisites("CSCI200")
        if "CSCI101" not in prereqs_200_after:
            print(" Prerequisite removal works correctly")
        else:
            print(" Prerequisite removal failed")
            return False
    
    db.close()
    print()
    return True

def test_delete():
    """ test deleting courses """
    print("=" * 70)
    print("TEST: DELETE Operations")
    print("=" * 70)
    print()
    
    db = DatabaseManager('test_crud.db', verbose=True)
    
    count_before = db.get_course_count()
    print(f"Courses before delete: {count_before}")
    
    # Delete a course
    success = db.delete_course("CSCI200")
    
    if success:
        count_after = db.get_course_count()
        print(f"Courses after delete: {count_after}")
        
        # Verify it's gone
        course = db.get_course_by_number("CSCI200")
        
        if course is None and count_after == count_before - 1:
            print("\n DELETE test PASSED")
        else:
            print("\n DELETE test FAILED - verification failed")
            return False
    else:
        print("\n DELETE test FAILED")
        return False
    
    db.close()
    print()
    return True

def cleanup():
    """ remove test database """
    test_db = Path('test_crud.db')
    if test_db.exists():
        test_db.unlink()
        print("Cleaned up test database")

if __name__ == "__main__":
    try:
        passed = []
        passed.append(test_create())
        passed.append(test_read())
        passed.append(test_update())
        passed.append(test_prerequisites())
        passed.append(test_delete())
        
        print("=" * 70)
        if all(passed):
            print("ALL CRUD TESTS PASSED")
        else:
            print(f"⚠ {sum(passed)}/{len(passed)} tests passed")
        print("=" * 70)
    except Exception as e:
        print(f"\nTEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()