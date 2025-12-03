# CS-499 Nick Valles
# Enhancement 3 - Module 5

"""
CLI interface for Course Planner

support commands using argparse for loading, listing and searching courses
Enhancement Three adds SQLite database support with parameterized queries

"""

import argparse
import sys
import traceback
from pathlib import Path
from typing import Optional

from .course_planner import CoursePlanner
from .config_manager import ConfigManager
from .database import DatabaseManager

class CoursePlannerCLI:
    """
    Command-Line-Interface (CLI) for Course Planner application

    Commands:
       
        - load: load course data from CSV file
        - migrate: migrate CSV data to SQLite database
        - list: display all courses in sorted order
        - search: find and display info about specific course
        - validate: validate prerequisites and check for circular dependencies
        - clear: clear out cached data
    
    """

    def __init__(self):
        """ initialize CLI with course planner instance"""
        
        self.planner = None
        self.config = ConfigManager()
        self.verbose = False
        self.use_database = False

    def _ensure_planner_loaded(self):
        """
        Ensure planner is loaded with data before command execution
    
        Tries to load from cache first (CSV mode), then checks for database
        """
        if self.planner is not None and self.planner.get_course_count() > 0:
            return  # loaded
    
        # check if database exists
        db_path = Path('course_catalog.db')
        if db_path.exists():
            # try database mode
            if self.verbose:
                print("Auto-loading from database...")
        self.planner = CoursePlanner(use_database=True, db_path='course_catalog.db')
        success = self.planner.load_from_database()
        if success and self.planner.get_course_count() > 0:
            return
    
        # try CSV mode with cache
        if self.planner is None:
            self.planner = CoursePlanner(use_database=False)
    
        # try loading from cache
        if self.planner.load_from_cache():
            if self.planner.get_course_count() > 0:
                if self.verbose:
                    print(f"Auto-loaded from cache: {self.planner.get_course_count()} courses")
                return
    
        # no data available
        print("No data loaded. Please run one of:")
        print("  python3 -m src load --database    # Load from database")
        print("  python3 -m src load                # Load from CSV")
        sys.exit(1)

    def load_command(self, args):
        """ 
        handles load command for loading courses from CSV
        
        --database flag: loads from SQLite database
        without flag: loads from CSV file 

        """
        
        self.use_database = args.database if hasattr(args, 'database') else False
        
        # initialize planner with appropriate mode
        if self.use_database:
            db_path = args.db_path if hasattr(args, 'db_path') and args.db_path else 'course_catalog.db'
            self.planner = CoursePlanner(use_database=True, db_path=db_path)
            
            if self.verbose:
                print(f"Database mode enabled: {db_path}")
                print("Loading courses from SQLite database...")
            
            try:
                success = self.planner.load_from_database()
                
                if success:
                    count = self.planner.get_course_count()
                    print(f"Successfully loaded {count} courses from database")
                else:
                    print("Failed to load courses from database")
                    print("Try running 'migrate' command first to populate the database")
                    sys.exit(1)
                    
            except Exception as e:
                print(f"Error loading from database: {e}")
                if self.verbose:
                    traceback.print_exc()
                sys.exit(1)
        
        else:
            # CSV mode
            self.planner = CoursePlanner(use_database=False)
            
            # determine file to load
            if args.file:
                filepath = args.file
                if self.verbose:
                    print(f"Loading from specified file: {filepath}")
            else:
                filepath = self.config.get_default_csv_path()
                if self.verbose:
                    print(f"Loading from default file: {filepath}")

            # attempt to load file
            try:
                success = self.planner.load_courses_from_csv(filepath)

                if success:
                    count = self.planner.get_course_count()
                    print(f"Successfully loaded {count} courses from {filepath}")
                    if self.verbose:
                        print("Data has been cached for future use")
                else:
                    print(f"Failed to load courses from {filepath}")
                    sys.exit(1)

            except FileNotFoundError as e:
                print(f"Error: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error: {e}")
                if self.verbose:
                    traceback.print_exc()
                sys.exit(1)


    def migrate_command(self, args):
        """
        handles migrate command for CSV to SQLite migration
        
        performs a complete ETL operation with transaction safety
        """
        
        if self.verbose:
            print("=" * 70)
            print("DATABASE MIGRATION: CSV -> SQLite")
            print("=" * 70)
            print()
        
        # determine source CSV file
        if args.file:
            csv_path = args.file
        else:
            csv_path = self.config.get_default_csv_path()
        
        # determine database path
        db_path = args.db_path if hasattr(args, 'db_path') and args.db_path else 'course_catalog.db'
        
        if self.verbose:
            print(f"Source CSV: {csv_path}")
            print(f"Target database: {db_path}")
            print()
            print("Starting migration...")
            print()
        
        try:
            # create database manager
            db = DatabaseManager(db_path, verbose=self.verbose)
            
            # CSV migration
            success, courses, prereqs = db.migrate_from_csv(csv_path)
            
            if success:
                print()
                print("=" * 70)
                print("MIGRATION SUCCESSFUL")
                print("=" * 70)
                print(f"Migrated {courses} courses")
                print(f"Migrated {prereqs} prerequisite relationships")
                print(f"Database: {db_path}")
                print()
                print("You can now use: python3 -m src load --database")
            else:
                print("Migration failed")
                sys.exit(1)
            
            db.close()
            
        except FileNotFoundError as e:
            print(f"Error: CSV file not found - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Migration error: {e}")
            if self.verbose:
                traceback.print_exc()
            sys.exit(1)


    def list_command(self, args):
        """ handles list command for displaying courses """
    
        # Auto-load data if needed
        self._ensure_planner_loaded()

        # get sorted courses
        courses = self.planner.get_sorted_courses()

        if self.verbose:
            mode = "database" if self.planner.use_database else "memory"
            print(f"Displaying {len(courses)} courses (source: {mode}):")
            print()

        print("Here is a sample schedule:")
        print()

        for course in courses:
            print(f"{course.course_number}, {course.name}")

        if self.verbose: 
            print()
            print(f"Total: {len(courses)} courses")

    def search_command(self, args):
        """ handle search command to find specific course """
    
        # auto-load data if needed
        self._ensure_planner_loaded()

        course_number = args.course_number

        if self.verbose:
            mode = "database" if self.planner.use_database else "memory"
            print(f"Searching for course: {course_number}")
            print(f"Data source: {mode}")
            if not self.planner.use_database:
                print("Using hash map index for O(1) lookup")
            else:
                print("Using parameterized SQL query with indexed lookup")
            print()

        # search using appropriate method
        if self.planner.use_database:
            # database query (parameterized for security)
            course = self.planner.db.get_course_by_number(course_number)
        else:
            # hash map lookup
            course = self.planner.find_course_fast(course_number)

        if course:
            # display course info
            print(f"{course.course_number}, {course.name}")

            if course.has_prerequisites():
                prereq_str = ", ".join(course.prerequisites)
                print(f"Prerequisites: {prereq_str}")
            else:
                print("Prerequisites: None")
        else:
            print(f"Course not found: {course_number}")
            if self.verbose:
                print("*Course numbers are case-insensitive*")

    def clear_command(self, args):
        """ handle the clear command to clear data cache """
        
        if not self.planner:
            self.planner = CoursePlanner(use_database=False)
        
        if self.planner.clear_cache():
            self.planner.courses.clear()
            print("Cache cleared successfully")
        else:
            print("Failed to clear cache")

    def validate_command(self, args):
        """ handle 'validate command to check prerequisites """
   
        # Auto-load data if needed
        self._ensure_planner_loaded()

        if self.verbose:
            print("Running prerequisite validation..")
            print("Checking for:" )
            print(" 1. non-existent prerequisites")
            print(" 2. circular dependencies")
            print()
    
        is_valid, errors = self.planner.validate_prerequisites()

        if is_valid:
            print("All prerequisites have been verified as valid")
            print(f" checked {self.planner.get_course_count()} courses")
            print(f" no circular dependencies found")
            print(f" all prerequisites exist in catalog")
        else:
            print(f"Found {len(errors)} issues with prerequisite") 
            print()
            for i, error in enumerate(errors, 1):
                print(f"{i}, {error}")
            sys.exit(1)

    def run(self, argv = None):
        """
        main entry for CLI application

        Args:
            argv: CLI arguments, defaults to sys.argv
            
        """

        parser=self._create_parser()
        args = parser.parse_args(argv)
        
        # verbose mode
        self.verbose = args.verbose

        if self.verbose:
            print(f"Course Planner CLI - Version {self.config.get_version()}")
            print()

        # exec appropriate command
        if hasattr(args, 'func'):
            args.func(args)
        else:
            # if no command is specified show help
            parser.print_help()
            sys.exit(1)

    def _create_parser(self) -> argparse.ArgumentParser:
        """ 
        create and config the argument parser

        Returns:
            configured ArgumentParser instance
            
        """

        # main parser
        parser = argparse.ArgumentParser(
            prog='course_planner',
            description='Course Planning and Prerequisite Catalog System',
            epilog='More info listed in the README.md file'
        )

        # glboal optional args
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='enable verbose output for debugging'
        )

        parser.add_argument(
            '--version',
            action='version',
            version=f"%(prog)s {self.config.get_version()}"
        )

        # subparsers for commands
        subparsers = parser.add_subparsers(
            title='commands',
            description='Available commands',
            dest='command',
            help='command to execute'
        )

        # load command
        load_parser = subparsers.add_parser(
            'load',
            help='load course data from CSV file',
            description='load course info from a CSV file into memory.'
        )

        load_parser.add_argument(
            '-f', '--file',
            type=str,
            help='path to CSV file (default is from config.ini)'
        )

        load_parser.add_argument(
            '--database',
            action='store_true',
            help='load from SQLite database instead of CSV'
        )
        
        load_parser.add_argument(
            '--db-path',
            type=str,
            default='course_catalog.db',
            help='path to database file (default: course_catalog.db)'
        )
            
        load_parser.set_defaults(func=self.load_command)

        # migrate command

        migrate_parser = subparsers.add_parser(
            'migrate',
            help='migrate CSV data to SQLite database',
            description='Perform ETL operation: Extract from CSV, Transform, Load to SQLite'
        )
        
        migrate_parser.add_argument(
            '-f', '--file',
            type=str,
            help='path to CSV file (default is from config.ini)'
        )
        
        migrate_parser.add_argument(
            '--db-path',
            type=str,
            default='course_catalog.db',
            help='path to database file (default: course_catalog.db)'
        )
        
        migrate_parser.set_defaults(func=self.migrate_command)

        # list command
        list_parser = subparsers.add_parser(
            'list',
            help='list all courses in alphabetical order',
            description='display all loaded courses sorted by course number.'
        )
        list_parser.set_defaults(func=self.list_command)

        # search command
        search_parser = subparsers.add_parser(
            'search',
            help='search for a specific course',
            description='find and display info about a course'
        )
        
        search_parser.add_argument(
            'course_number',
            type=str,
            help='course number to search for (e.g, CS101)'
        )
        search_parser.set_defaults(func=self.search_command)

        # validate command 
        validate_parser = subparsers.add_parser(
            "validate",
            help='Validate course prerequisites',
            description='Check for circular dependencies'
        )
        validate_parser.set_defaults(func=self.validate_command)

        # clear command
        clear_parser = subparsers.add_parser(
            'clear',
            help='Clear cached course data',
            description='Remove the cached course data file'
        )
        clear_parser.set_defaults(func=self.clear_command)

        return parser

def main():
    """ main entry point for application """
        
    cli = CoursePlannerCLI()
    cli.run()

if __name__ == '__main__':
    main()