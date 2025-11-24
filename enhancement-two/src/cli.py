# CS-499 Nick Valles
# Enhancement 2 - Module 4

"""
CLI interface for Course Planner

support commands using argparse for loading, listing and searching courses

"""

import argparse
import sys
import traceback
from pathlib import Path
from typing import Optional

from .course_planner import CoursePlanner
from .config_manager import ConfigManager

class CoursePlannerCLI:
    """
    Command-Line-Interface (CLI) for Course Planner application

    Commands:
       
        - load: load course data from CSV file
        - list: display all courses in sorted order
        - search: find and display info about specific course
    
    """

    def __init__(self):
        """ initialize CLI with course planner instance"""
        
        self.planner = CoursePlanner()
        self.config = ConfigManager()
        self.verbose = False

        # attempt loading from cache
        if self.planner.load_from_cache():
            if self.verbose:
                print(f"Loaded {self.planner.get_course_count()} courses from cache")

    def load_command(self, args):
        """ handles load command for loading courses from CSV """
        
        # determining file to load
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
                    print("Data has been cached for future")
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

    def list_command(self, args):
        """ handles list command for displaying courses """

        if self.planner.get_course_count() == 0:
            print("No courses loaded, please run 'load' command first")
            sys.exit(1)

        # get sorted courses
        courses = self.planner.get_sorted_courses()

        if self.verbose:
            print(f"Displaying {len(courses)} courses:")
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

        if self.planner.get_course_count() == 0:
            print("No courses loaded, please run 'load' command first")
            sys.exit(1)

        course_number = args.course_number

        if self.verbose:
            print(f"Searching for course: {course_number}")
            print("Using hash map index for O(1) lookup")
            print()

        # find course (linear)
        # course = self.planner.find_course(course_number)
        # find course (hash map)
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
        if self.planner.clear_cache():
            self.planner.courses.clear()
            print("Cache cleared successfully")
        else:
            print("Failed to clear cache")

    def validate_command(self, args):
        """ handle 'validate command to check prerequisites """
        if self.planner.get_course_count() == 0:
            print("No courses have been loaded, run 'load' command first")
            sys.exit(1)

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
            
        load_parser.set_defaults(func=self.load_command)

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