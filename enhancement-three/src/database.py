# CS-499 Nick Valles
# Enhancement 3 - Module 5

"""
Database management for Course Planner

handles SQLite database operations including schema creation,
data migration, and CRUD operations within transaction management

"""

import sqlite3
import csv
from pathlib import Path
from typing import List, Optional, Tuple
from contextlib import contextmanager

from .models import Course

class DatabaseManager:
    """
    provides connection management, schema creation, data migration,
    and CRUD operations with proper transaction handling for SQLite operations

    """
    def __init__(self, db_path: str = 'course_catalog.db', verbose: bool = False):
        """
        initialize database manager

        Args: 
            db_path: path to SQLite database file
            verbose: enabling verbose input for operations
        """
        
        self.db_path = db_path
        self.verbose = verbose
        self._connection = None

    def connect(self) -> sqlite3.Connection:
        """
        establish database connection

        Returns:
            SQLite connection object

        """

        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row # enable column access by name
        return self._connection

    def close(self):
        """closing database connection"""

        if self._connection:
            self._connection.close()
            self._connection = None

    @contextmanager
    def transaction(self):
        """
        context manager for database transactions

        automatically commit on success, roll back on error

        Usage:
            with db.transaction():
                    db.execute_query(...)
        
        """

        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

    def create_schema(self) -> bool:
        """
        create database schema for course catalog

        Schema Design:
            courses: main course info table
            prerequisites: junction table for many-to-many relationships

        Returns:
            True if schema created succesfully

        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()

            # create courses table

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses(
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_number TEXT UNIQUE NOT NULL,
                    course_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # create prerequisites junction table

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prerequisites (
                    prerequisite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    prerequisite_course_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                    FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                    UNIQUE(course_id, prerequisite_course_id)
                )
            ''')
                
            # create indexes for performance
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_course_number 
                ON courses(course_number)
            ''')
                
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_prerequisites_course 
                ON prerequisites(course_id)
            ''')
                
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_prerequisites_prereq 
                ON prerequisites(prerequisite_course_id)
            ''')
                
            print("database schema created successfully")
            return True
                
        except sqlite3.Error as e:
            print(f"error creating schema: {e}")
            return False

    def drop_schema(self) -> bool:
        """
        drop all tables (for testing/reset)

        Returns:
            True if schema dropped successfully

        """

        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute('DROP TABLE IF EXISTS prerequisites')
                cursor.execute('DROP TABLE IF EXISTS courses')
                print("database schema has been dropped")

                return True

        except sqlite3.Error as e:
            print(f"Error dropping schema: {e}")
            return False

    def migrate_from_csv(self, csv_path: str) -> Tuple[bool, int, int]:
        """
        migrate course data from CSV file to SQlite database
        
        performs extraction, transformation and loading (ETL) operation:
            extract data from CSV
            transform via parsing and validating course data
            load by inserting into database with transaction safety
        
        Args:
            csv_path: path to CSV file containing course data

        Returns:
            tuple of (success, courses_inserted, prerequisites_inserted)

        """
        courses_inserted = 0
        prerequisites_inserted = 0

        try:
            # ensuring schema exists
            self.create_schema()

            # reading csv
            file_path = Path(csv_path)
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_path}")

            courses_data = []
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or all(field.strip() == '' for field in row):
                        continue
                    if len(row) < 2:
                        continue

                    course_number = row[0].strip().upper()
                    course_name = row[1].strip()
                    prerequisites = [p.strip().upper() for p in row[2:] if p.strip()]
                    
                    courses_data.append((course_number, course_name, prerequisites))

            # migrate data in a single transaction
            with self.transaction() as conn:
                cursor = conn.cursor()

                # clear existing data
                cursor.execute('DELETE FROM prerequisites')
                cursor.execute('DELETE FROM courses')
                
                # insert courses
                for course_number, course_name, _ in courses_data:
                    cursor.execute('''
                        INSERT INTO courses (course_number, course_name)
                        VALUES (?, ?)
                    ''', (course_number, course_name))
                    courses_inserted += 1
                
                # build course_id lookup
                cursor.execute('SELECT course_id, course_number FROM courses')
                course_id_map = {row['course_number']: row['course_id'] for row in cursor.fetchall()}
                
                # insert prerequisites
                for course_number, _, prerequisites in courses_data:
                    course_id = course_id_map[course_number]
                    
                    for prereq_number in prerequisites:
                        if prereq_number in course_id_map:
                            prereq_id = course_id_map[prereq_number]
                            cursor.execute('''
                                INSERT INTO prerequisites (course_id, prerequisite_course_id)
                                VALUES (?, ?)
                            ''', (course_id, prereq_id))
                            prerequisites_inserted += 1
                        else:
                            print(f"Warning: Prerequisite {prereq_number} not found for {course_number}")
            
            print(f"Migration complete: {courses_inserted} courses, {prerequisites_inserted} prerequisites")
            return True, courses_inserted, prerequisites_inserted
            
        except Exception as e:
            print(f"Error during migration: {e}")
            return False, 0, 0
    
    def get_all_courses(self) -> List[Course]:
        """
        retrieve all courses from database
        
        Returns:
            list of Course objects
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # fet all courses
            cursor.execute('''
                SELECT course_id, course_number, course_name 
                FROM courses 
                ORDER BY course_number
            ''')
            
            courses = []
            for row in cursor.fetchall():
                course_id = row['course_id']
                course_number = row['course_number']
                course_name = row['course_name']
                
                # get prerequisites for this course
                cursor.execute('''
                    SELECT c.course_number
                    FROM prerequisites p
                    JOIN courses c ON p.prerequisite_course_id = c.course_id
                    WHERE p.course_id = ?
                    ORDER BY c.course_number
                ''', (course_id,))
                
                prerequisites = [row['course_number'] for row in cursor.fetchall()]
                
                courses.append(Course(
                    course_number=course_number,
                    name=course_name,
                    prerequisites=prerequisites
                ))
            
            return courses
            
        except sqlite3.Error as e:
            print(f"Error retrieving courses: {e}")
            return []
    
    def get_course_by_number(self, course_number: str) -> Optional[Course]:
        """
        retrieve a specific course by its course number
        
        Args:
            course_number - course number to search for
            
        Returns:
            course object if found, None otherwise
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            search_number = course_number.strip().upper()
            
            # get course
            cursor.execute('''
                SELECT course_id, course_number, course_name
                FROM courses
                WHERE course_number = ?
            ''', (search_number,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            course_id = row['course_id']
            course_number = row['course_number']
            course_name = row['course_name']
            
            # get prerequisites
            cursor.execute('''
                SELECT c.course_number
                FROM prerequisites p
                JOIN courses c ON p.prerequisite_course_id = c.course_id
                WHERE p.course_id = ?
                ORDER BY c.course_number
            ''', (course_id,))
            
            prerequisites = [row['course_number'] for row in cursor.fetchall()]
            
            return Course(
                course_number=course_number,
                name=course_name,
                prerequisites=prerequisites
            )
            
        except sqlite3.Error as e:
            print(f"Error retrieving course: {e}")
            return None
    
    def get_course_count(self) -> int:
        """
        get total number of courses in database
        
        Returns:
            Number of courses
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM courses')
            return cursor.fetchone()['count']
        except sqlite3.Error as e:
            print(f"Error counting courses: {e}")
            return 0
    
    # crud operations
    
    def add_course(self, course_number: str, course_name: str) -> Optional[int]:
        """
        create a new course in the database
        
        Args:
            course_number: course identifier (e.g., CSCI101)
            course_name: name of the course
            
        Returns:
            course_id if successful, None otherwise
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                
                course_number = course_number.strip().upper()
                course_name = course_name.strip()
                
                cursor.execute('''
                    INSERT INTO courses (course_number, course_name)
                    VALUES (?, ?)
                ''', (course_number, course_name))
                
                course_id = cursor.lastrowid
                
                if self.verbose:
                    print(f"Added course: {course_number} - {course_name} (ID: {course_id})")
                
                return course_id
                
        except sqlite3.IntegrityError:
            print(f"Error: Course {course_number} already exists")
            return None
        except sqlite3.Error as e:
            print(f"Error adding course: {e}")
            return None
    
    def update_course(self, course_number: str, new_name: str) -> bool:
        """
        update an existing course name
        
        Args:
            course_number: course to update
            new_name: new course name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                
                course_number = course_number.strip().upper()
                new_name = new_name.strip()
                
                cursor.execute('''
                    UPDATE courses 
                    SET course_name = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE course_number = ?
                ''', (new_name, course_number))
                
                if cursor.rowcount == 0:
                    print(f"Error: Course {course_number} not found")
                    return False
                
                if self.verbose:
                    print(f"Updated course {course_number} name to: {new_name}")
                
                return True
                
        except sqlite3.Error as e:
            print(f"Error updating course: {e}")
            return False
    
    def delete_course(self, course_number: str) -> bool:
        """
        delete a course from the database
        
        prerequisites are automatically deleted due to CASCADE
        
        Args:
            course_number: Course to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                
                course_number = course_number.strip().upper()
                
                cursor.execute('''
                    DELETE FROM courses WHERE course_number = ?
                ''', (course_number,))
                
                if cursor.rowcount == 0:
                    print(f"Error: Course {course_number} not found")
                    return False
                
                if self.verbose:
                    print(f"Deleted course: {course_number}")
                
                return True
                
        except sqlite3.Error as e:
            print(f"Error deleting course: {e}")
            return False
    
    def add_prerequisite(self, course_number: str, prerequisite_number: str) -> bool:
        """
        add a prerequisite relationship between courses
        
        Args:
            course_number: course that requires the prerequisite
            prerequisite_number: course that is the prerequisite
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                
                course_number = course_number.strip().upper()
                prerequisite_number = prerequisite_number.strip().upper()
                
                # course IDs
                cursor.execute('SELECT course_id FROM courses WHERE course_number = ?', 
                             (course_number,))
                course_row = cursor.fetchone()
                
                cursor.execute('SELECT course_id FROM courses WHERE course_number = ?', 
                             (prerequisite_number,))
                prereq_row = cursor.fetchone()
                
                if not course_row:
                    print(f"Error: Course {course_number} not found")
                    return False
                if not prereq_row:
                    print(f"Error: Prerequisite {prerequisite_number} not found")
                    return False
                
                course_id = course_row['course_id']
                prereq_id = prereq_row['course_id']
                
                cursor.execute('''
                    INSERT INTO prerequisites (course_id, prerequisite_course_id)
                    VALUES (?, ?)
                ''', (course_id, prereq_id))
                
                if self.verbose:
                    print(f"Added prerequisite: {course_number} requires {prerequisite_number}")
                
                return True
                
        except sqlite3.IntegrityError:
            print(f"Error: Prerequisite relationship already exists")
            return False
        except sqlite3.Error as e:
            print(f"Error adding prerequisite: {e}")
            return False
    
    def remove_prerequisite(self, course_number: str, prerequisite_number: str) -> bool:
        """
        Remove a prerequisite relationship
        
        Args:
            course_number: Course that requires the prerequisite
            prerequisite_number: Prerequisite to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                
                course_number = course_number.strip().upper()
                prerequisite_number = prerequisite_number.strip().upper()
                
                # course IDs
                cursor.execute('SELECT course_id FROM courses WHERE course_number = ?', 
                             (course_number,))
                course_row = cursor.fetchone()
                
                cursor.execute('SELECT course_id FROM courses WHERE course_number = ?', 
                             (prerequisite_number,))
                prereq_row = cursor.fetchone()
                
                if not course_row or not prereq_row:
                    print(f"Error: Course not found")
                    return False
                
                course_id = course_row['course_id']
                prereq_id = prereq_row['course_id']
                
                cursor.execute('''
                    DELETE FROM prerequisites 
                    WHERE course_id = ? AND prerequisite_course_id = ?
                ''', (course_id, prereq_id))
                
                if cursor.rowcount == 0:
                    print(f"Error: Prerequisite relationship not found")
                    return False
                
                if self.verbose:
                    print(f"Removed prerequisite: {course_number} no longer requires {prerequisite_number}")
                
                return True
                
        except sqlite3.Error as e:
            print(f"Error removing prerequisite: {e}")
            return False
    
    def get_prerequisites(self, course_number: str) -> List[str]:
        """
        get all prerequisites for a specific course
        
        Args:
            course_number: Course to get prerequisites for
            
        Returns:
            list of prerequisite course numbers
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            course_number = course_number.strip().upper()
            
            cursor.execute('''
                SELECT c.course_number
                FROM prerequisites p
                JOIN courses c1 ON p.course_id = c1.course_id
                JOIN courses c ON p.prerequisite_course_id = c.course_id
                WHERE c1.course_number = ?
                ORDER BY c.course_number
            ''', (course_number,))
            
            return [row['course_number'] for row in cursor.fetchall()]
            
        except sqlite3.Error as e:
            print(f"Error getting prerequisites: {e}")
            return []