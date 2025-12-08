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
from .logger import LoggerConfig, get_logger

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
        """ initialize CLI with course planner instance """
    
        self.planner = None
        self.config = ConfigManager()
        self.verbose = False
        self.use_database = False
    
        # initialize logging from config
        LoggerConfig.setup_logging(
            level=self.config.get_log_level(),
            log_to_file=self.config.get_log_to_file(),
            log_file=self.config.get_log_file(),
            format_style=self.config.get_log_format_style()
        )
    
        self.logger = get_logger()

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
        
            self.logger.debug(f"Database mode enabled: {db_path}")
            self.logger.info("Loading courses from SQLite database...")
        
            try:
                success = self.planner.load_from_database()
            
                if success:
                    count = self.planner.get_course_count()
                    self.logger.info(f"Successfully loaded {count} courses from database")
                    print(f"Successfully loaded {count} courses from database")
                else:
                    self.logger.error("Failed to load courses from database")
                    print("Failed to load courses from database")
                    print("Try running 'migrate' command first to populate the database")
                    sys.exit(1)
                
            except Exception as e:
                self.logger.error(f"Error loading from database: {e}", exc_info=True)
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
                self.logger.debug(f"Loading from specified file: {filepath}")
            else:
                filepath = self.config.get_default_csv_path()
                self.logger.debug(f"Loading from default file: {filepath}")

            # attempt to load file
            try:
                success = self.planner.load_courses_from_csv(filepath)

                if success:
                    count = self.planner.get_course_count()
                    self.logger.info(f"Successfully loaded {count} courses from {filepath}")
                    print(f"Successfully loaded {count} courses from {filepath}")
                    if self.verbose:
                        print("Data has been cached for future use")
                else:
                    self.logger.error(f"Failed to load courses from {filepath}")
                    print(f"Failed to load courses from {filepath}")
                    sys.exit(1)

            except FileNotFoundError as e:
                self.logger.error(f"File not found: {e}")
                print(f"Error: {e}")
                sys.exit(1)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}", exc_info=True)
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
            print("DATABASE MIGRATION: CSV → SQLite")
            print("=" * 70)
            print()
    
        # determine source CSV file
        if args.file:
            csv_path = args.file
        else:
            csv_path = self.config.get_default_csv_path()
    
        # determine database path
        db_path = args.db_path if hasattr(args, 'db_path') and args.db_path else 'course_catalog.db'
    
        self.logger.info(f"Starting migration: {csv_path} → {db_path}")
    
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
                self.logger.info(f"Migration successful: {courses} courses, {prereqs} prerequisites")
                print()
                print("=" * 70)
                print("Migration Successful")
                print("=" * 70)
                print(f"Migrated {courses} courses")
                print(f"Migrated {prereqs} prerequisite relationships")
                print(f"Database: {db_path}")
                print()
                print("You can now use: python3 -m src load --database")
            else:
                self.logger.error("Migration failed")
                print("Migration failed")
                sys.exit(1)
        
            db.close()
        
        except FileNotFoundError as e:
            self.logger.error(f"CSV file not found: {e}")
            print(f"Error: CSV file not found - {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Migration error: {e}", exc_info=True)
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
    
        # Auto-load data if needed
        self._ensure_planner_loaded()

        course_number = args.course_number
    
        self.logger.debug(f"Searching for course: {course_number}")

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
            self.logger.debug(f"Course found: {course.course_number}")
            # display course info
            print(f"{course.course_number}, {course.name}")

            if course.has_prerequisites():
                prereq_str = ", ".join(course.prerequisites)
                print(f"Prerequisites: {prereq_str}")
            else:
                print("Prerequisites: None")
        else:
            self.logger.warning(f"Course not found: {course_number}")
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

    def prereq_chain_command(self, args):
        """ handle prerequisite-chain command to show all indirect prerequisites """
    
        # auto-load data if needed
        self._ensure_planner_loaded()
    
        course_number = args.course_number
    
        self.logger.info(f"Analyzing prerequisite chain for {course_number}")
    
        if not self.planner.use_database:
            print("Prerequisite chain analysis requires database mode")
            print("Please run: python3 -m src load --database")
            sys.exit(1)
    
        # get full prerequisite chain
        result = self.planner.db.get_full_prerequisite_chain(course_number)
    
        if 'error' in result:
            self.logger.error(f"Error: {result['error']}")
            print(f"Error: {result['error']}")
            sys.exit(1)
    
        # display results
        course = result['course']
        total = result['total_prerequisites']
        max_depth = result['max_depth']
        levels = result['levels']
    
        print("=" * 70)
        print(f"PREREQUISITE CHAIN ANALYSIS")
        print("=" * 70)
        print()
        print(f"Course: {course['number']} - {course['name']}")
        print(f"Total Prerequisites (direct + indirect): {total}")
        print(f"Maximum Depth: {max_depth} level(s)")
        print()
    
        if total == 0:
            print("This course has no prerequisites")
            return
    
        # display by level
        for level in sorted(levels.keys()):
            courses = levels[level]
            level_name = "Direct Prerequisites" if level == 1 else f"Level {level} Prerequisites"
            print(f"{level_name}:")
            print("-" * 70)
        
            for course_info in courses:
                indent = "  " * (level - 1)
                print(f"{indent}→ {course_info['course_number']}: {course_info['course_name']}")
        
            print()
    
        # show visualization
        if self.verbose:
            print("Prerequisite Tree Visualization:")
            print("-" * 70)
            self._print_prereq_tree(course_number, levels, max_depth)

    def _print_prereq_tree(self, root_course: str, levels: dict, max_depth: int):
        """ helper function to print tree visualization """
        print(f"{root_course}")
    
        for level in sorted(levels.keys()):
            courses = levels[level]
            indent = "  " * level
            prefix = "└──" if level == max_depth else "├──"
        
            for i, course_info in enumerate(courses):
                is_last = (i == len(courses) - 1) and (level == max_depth)
                connector = "└──" if is_last else "├──"
                print(f"{indent}{connector} {course_info['course_number']}")

    def run(self, argv = None):
        """
        main entry for CLI application

        Args:
            argv: CLI arguments, defaults to sys.argv
        """

        parser = self._create_parser()
        args = parser.parse_args(argv)
    
        # verbose mode
        self.verbose = args.verbose
    
        if self.verbose:
            LoggerConfig.enable_verbose()
            self.logger.debug("Verbose mode enabled")
            print(f"Course Planner CLI - Version {self.config.get_version()}")
            print()

        self.logger.info("CLI started")
    
        # exec appropriate command
        if hasattr(args, 'func'):
            self.logger.debug(f"Executing command: {args.command}")
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

        # prerequisite chain command (recursive CTE)
        prereq_chain_parser = subparsers.add_parser(
            'prereq-chain',
            help='Show complete prerequisite chain (recursive)',
            description='Display all direct and indirect prerequisites using recursive SQL query'
        )

        prereq_chain_parser.add_argument(
            'course_number',
            type=str,
            help='course number to analyze (e.g., CS400)'
        )
        prereq_chain_parser.set_defaults(func=self.prereq_chain_command)

        return parser

def main():
    """ main entry point for application """
        
    cli = CoursePlannerCLI()
    cli.run()

if __name__ == '__main__':
    main()