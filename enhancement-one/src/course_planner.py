# CS-499 Nick Valles
# Enhancement 1 - Module 3

"""
core planner logic for course planning operations

"""

import csv
import pickle
from typing import List, Optional
from pathlib import Path

from .models import Course

class CoursePlanner:
    """
    manage course data and provide operations for course planning 

    CoursePlanner handles loading course data from CSV files and provides 
    methods to query and display course info.

    """

    # hidden cache 
    CACHE_FILE = '.course_cache.pkl'

    def __init__(self):
        """ initialize course planner with empty course list """
        
        self.courses: List[Course] = []

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

        # clear existing courses
        self.courses.clear()

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
            return True
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
        find a course by its course number
        *TODO this currently uses the linear search - will
        optimize in next enhancment

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

    def get_sorted_courses(self) -> List[Course]:
        """
        Get all courses sorted by course number

        Returns:
            List of courses sorted alphabetically by course number
            
        """

        return sorted(self.courses, key=lambda c: c.course_number)