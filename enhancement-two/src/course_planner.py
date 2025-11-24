# CS-499 Nick Valles
# Enhancement 2 - Module 4

"""
core planner logic for course planning operations

enhanced with hash map indexing for O(1) course lookups

"""

import csv
import pickle
from typing import List, Optional, Dict
from pathlib import Path

from .models import Course

class CoursePlanner:
    """
    manage course data and provide operations for course planning 

    CoursePlanner handles loading course data from CSV files and provides 
    methods to query and display course info.

    Enhancement Two adds hash map indexing for O(1) lookups

    """

    # hidden cache 
    CACHE_FILE = '.course_cache.pkl'

    def __init__(self):
        """ initialize course planner with empty course list """
        
        self.courses: List[Course] = []
        self.course_index: Dict[str, Course] = {} # Hashmap implementation

    def build_index(self) -> None:
        """
        build hash map index for faster O(1) course lookups

        create a dictionary that maps course numbers to Course objects,
        changing lookup time complexity from O(n) to O(1) 

        """
        self.course_index.clear()

        for course in self.courses:
            # use uppercase course number as key for case insensitive lookup
            self.course_index[course.course_number] = course

        # course_number is already uppercase from Course.__post_init__

    def load_courses_from_csv(self, filepath: str) -> bool:
        """
        load course data from csv file

        Expected CSV formatting:
            CourseNumber,CourseName,Prerequisite1,Prerequisite2,...
        
        Args:
            filepath: path to CSV file
            
        Returns: 
            True if loading succeeded, False otherwise

        Raises:
            FileNotFoundError: if CSV file doesn't exist
            PermissionError: if file can't be read with current permissions
            ValueError: if CSV format isn't correct

        """

        file_path = Path(filepath)

        # check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        # check if file is readable
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {filepath}")

        # clear existing courses
        self.courses.clear()
        self.course_index.clear()

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)

                for line_num, row in enumerate(reader, start=1):
                    # skip empty lines
                    if not row or all(field.strip() == '' for field in row):
                        continue
                    
                    # validate minimum required fields
                    if len(row) < 2:
                        print(f"Warning: Line {line_num} has invalid format (need at least course number and name)")
                        continue

                    # parsing course data
                    course_number = row[0].strip()
                    course_name = row[1].strip()
                    prerequisites = [p.strip() for p in row[2:] if p.strip()]

                    # creating Course object, dataclass handles further cleaning 
                    course = Course(
                        course_number=course_number,
                        name=course_name,
                        prerequisites=prerequisites
                    )

                    self.courses.append(course)
            
            # build hash map index after successful load
            self.build_index()

            # validate prerequisites afer loading 
            is_valid, errors = self.validate_prerequisites()
            if not is_valid:
                print("\n Warning: prerequisite validation found issues:")
                for error in errors:
                    print(f" - {error}")
                print()

            # save to cache after successful load
            self._save_cache()        

            return True

        except PermissionError as e:
            print(f"Error: Permission denied reading file: {filepath}")
            return False
        except csv.Error as e:
            print(f"Error: Invalid CSV format {e}")
            return False     
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return False
        
    # need cache otherwise Python cmds don't stay persistent, pickle should work for this purpose
    def _save_cache(self) -> bool:
        """
        save courses to cache file for persistence
        
        Returns:
            True if save succeeded, False otherwise
        
        """

        try:
            with open(self.CACHE_FILE, 'wb') as f:
                pickle.dump(self.courses, f)
            return True
        except PermissionError:
            print(f"Warning: Permission denied writing cache file")
            return False
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")
            return False
        except Exception as e:
            print(f"Warning: Unexpected error saving cache: {e}")
            return False
    
    def load_from_cache(self) -> bool:
        """
        load courses from cache file if it exists
        
        Returns:
            True if cache loaded successfully, False otherwise
        
        """

        cache_path = Path(self.CACHE_FILE)
        
        if not cache_path.exists():
            return False
        
        try:
            with open(self.CACHE_FILE, 'rb') as f:
                self.courses = pickle.load(f)
            
            # rebuild index after loading from cache    
            self.build_index()
            return True

        except PermissionError:
            print(f"Warning: Permission denied reading cache file")
            return False
        except pickle.UnpicklingError:
            print(f"Warning: Cache file corrupted, please run 'load' again")
            # clear corrupted cache
            self.clear_cache()
            return False
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")
            return False
    
    def clear_cache(self) -> bool:
        """
        clears the cache file
        
        Returns:
            True if cache cleared successfully, False otherwise
       
        """

        cache_path = Path(self.CACHE_FILE)
        
        if cache_path.exists():
            try:
                cache_path.unlink()
                return True
            
            except PermissionError:
                print(f"Warning: Permission denied reading cache file")
                return False
            except pickle.UnpicklingError:
                print(f"Warning: Cache file has been corrupted, please run 'load' command again")
            except Exception as e:
                print(f"Warning: Could not clear cache: {e}")
                return False
        return True

    def get_all_courses(self) -> List[Course]:
        """
        get all loaded courses

        Returns:
            list of all Course objects
            
        """

        return self.courses.copy()

    def get_course_count(self) -> int:
        """
        get number of loaded courses

        Returns:
            number of courses currently loaded
            
        """

        return len(self.courses)

    def find_course(self, course_number: str) -> Optional[Course]:
        """
        find a course by its course number (linear search)
        
        old O(n) method kept for comparison purposes, 
        use find_course_fast() for O(1) performance

        Args:
            course_number: course number to search for

        Returns:
            course object if found, None otherwise

        """

        search_number= course_number.strip().upper()

        for course in self.courses:
            if course.course_number == search_number:
                return course

        return None

    def find_course_fast(self, course_number: str) -> Optional[Course]:
        """
        find a course by its course number (hash map lookup)
        
        optimized O(1) method using hash map index

        Args:
            course_number: course number to search for

        Returns:
            course object if found, None otherwise

        """

        search_number = course_number.strip().upper()
        return self.course_index.get(search_number)

    def get_sorted_courses(self) -> List[Course]:
        """
        Get all courses sorted by course number

        Returns:
            List of courses sorted alphabetically by course number
            
        """

        return sorted(self.courses, key=lambda c: c.course_number)

    def validate_prerequisites(self) -> tuple[bool, list[str]]:
        """
        detect cycles using depth-first search (DFS)

        check for:
            1. circular dependencies (cycles in prereq graph)
            2. prereqs that do not exist within course catalog

        Returns:
            tuple: (is_valid, list_of_errors)
                is_valid: True if all prerequisites are valid
                list_of_errors: list of error messages (empty if valid)


        """
        errors = []

        # initial check validates that all prerequisites exist
        for course in self.courses:
            for prereq in course.prerequisites:
                if prereq not in self.course_index:
                    errors.append(
                        f"Course {course.course_number} lists prerequisite "
                        f"{prereq} which does not exist in catalog"
                    )

        # second check detects circular dependencies using DFS
        visited = set()
        in_progress = set()
        reported_cycles = set()

        for course in self.courses:
            if course.course_number not in visited:
                cycle_error = self._detect_cycle_dfs(
                    course.course_number,
                    visited,
                    in_progress,
                    reported_cycles
                )
                if cycle_error:
                    errors.append(cycle_error)
        
        is_valid = len(errors) == 0
        return is_valid, errors

    def _detect_cycle_dfs(
        self,
        course_number: str,
        visited: set,
        in_progress: set,
        reported_cycles: set
    ) -> Optional[str]:
        """

        detecting cycles via Depth-First Search (DFS)

        uses two sets to track state:
            visited: Courses that have been fully processed
            in_progress: courses currently in DFS path (recursion stack)

        if course encountered in_progress, cycle has been found

        Args:
            course_number: current course being examined
            visited: set of fully processed courses
            in_progress: set of courses in current DFS path

        Returns: error message string if cycle found, None otherwise

        """

        # mark this course as being processed
        in_progress.add(course_number)

        # getting course object
        course = self.course_index.get(course_number)

        if not course:
            # course doesn't exist, caught by validate_prequisites
            in_progress.remove(course_number)
            visited.add(course_number)
            return None

        # check each prerequisite
        for prereq_number in course.prerequisites:
            # if prerequisite doesn't exist, skip
            if prereq_number not in self.course_index:
                continue
        
            # if prerequisite is in current path, cycle found
            if prereq_number in in_progress:

                cycle_pair = tuple(sorted([course_number, prereq_number]))
                if cycle_pair not in reported_cycles:
                    reported_cycles.add(cycle_pair)
                    # build cycle path for error message
                    return (
                        f"Circular dependency detected: {course_number} requires "
                        f"{prereq_number}, which is not possible"
                    )
                return None # if we forget this infinite loop haha
        
            # prerequisite hasn't been fully checked, recursively check it
            if prereq_number not in visited:
                cycle_error = self._detect_cycle_dfs(
                    prereq_number, 
                    visited, 
                    in_progress,
                    reported_cycles
                )
                if cycle_error:
                    return cycle_error
    
        # finished processing this course, remove from current path
        in_progress.remove(course_number)
        # mark as fully processed
        visited.add(course_number)

        return None

    def has_circular_dependency(self) -> bool:
        """
        check if circular dependency exists
        wrapper around validate_prerequisites() made for convenience
        for when yes/no answer is the only thing needed

        Returns:
            True if circular dependency exists, False otherwise

        """

        is_valid, errors = self.validate_prerequisites()

        # check if any errors mention "circular dependency"
        for error in errors:
            if "Circular dependency" in error or "cycle" in error.lower():
                return True
        
        return False