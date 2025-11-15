# CS-499 Nick Valles
# Enhancement 1 - Module 3

"""
data models for Course Planner application

"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Course:
    """
    represent course in the course catalog

    Attributes:
    course_number: acts as a unique identifier for course (e.g CS101)
    name: full name of course (e.g Intro to Programming)
    prerequisites: list of course numbers that are prerequisites
   
    """

    course_number: str
    name: str
    prerequisites: List[str] = field(default_factory=list)

    def __post_init__(self):
        """
        post-init processing for cleaning & validating data
        converts course number to uppercase and strips whitespace
        filters out empty prerequisite strings
        
        """

        # clean course number
        self.course_number = self.course_number.strip().upper()

        # clean course name
        self.name = self.name.strip()

        # clean/filter prerequisites
        self.prerequisites = [
            prereq.strip().upper()
            for prereq in self.prerequisites
            if prereq.strip()
        ]

    def has_prerequisites(self) -> bool:
        """
        checks if course has prerequisites

        Returns:
            True if course has prerequisites, False if not
        
        """
        
        return len(self.prerequisites) > 0

    def __str__(self) -> str:
        """
        string representation of the course

        Returns:
            formatted string with course number and name
       
        """

        return f"{self.course_number}, {self.name}"