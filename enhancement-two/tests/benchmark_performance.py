# CS-499 Nick Valles
# Enhancement 2 - Module 4

"""
Performance benchmarking for hash map vs linear search

Demonstrate the O(1) vs O(n) time complexity improvement

"""

import sys
import time
from pathlib import Path

# add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.course_planner import CoursePlanner

def benchmark_search_methods(iterations: int = 1000):
    """
    benchmark linear search vs hash map lookup performance

    Args:
        iterations: Number of search iterations to perform

    """

    print("=" * 70)
    print("PERFORMANCE BENCHMARK: Linear Search vs Hash Map Lookup")
    print("=" * 70)
    print()

    # loading test data
    planner = CoursePlanner()
    csv_path = Path(__file__).parent.parent / 'data' / 'CS_300_ABCU_Advising_Program_Input.csv'
    planner.load_courses_from_csv(str(csv_path))

    num_courses = planner.get_course_count()
    print(f"Dataset: {num_courses} courses")
    print(f"Iterations: {iterations:,} searches per method")
    print()

    # test courses to search for 
    test_courses = ["CS101", "CS102", "CS103", "CS104"]

    # benchmark 1: Linear search 0(n)
    print("Testing linear search (O(n)):")
    start_time = time.perf_counter()

    for _ in range(iterations):
        for course_num in test_courses:
            result = planner.find_course(course_num)

    linear_time = time.perf_counter() - start_time
    linear_avg = (linear_time / (iterations * len(test_courses))) * 1_000_000 # microseconds

    print(f" Total time: {linear_time:.4f} seconds")
    print(f" Average per search: {linear_avg:.2f} microseconds")
    print()

    # benchmark 2: hash map lookup (0)1
    print("Testing hash map lookup (0(1)):")
    start_time = time.perf_counter()

    for _ in range(iterations):
        for course_num in test_courses:
            result = planner.find_course_fast(course_num)
    
    hashmap_time = time.perf_counter() - start_time
    hashmap_avg = (hashmap_time / (iterations * len(test_courses))) * 1_000_000 # microseconds

    print(f" total time: {hashmap_time:.4f} seconds")
    print(f" Average per search: {hashmap_avg:.2f} microseconds")
    print()

    # calculate improvement 
    speedup = linear_time / hashmap_time
    improvement = ((linear_time - hashmap_time) / linear_time) * 100

    print("=" * 70)
    print("results")
    print("=" * 70)
    print(f"speed up factor: {speedup:.2f}x faster")
    print(f"performance improvement: {improvement:.1f}%")
    print()

    # analysis
    print("analysis")
    print("-" * 70)
    print(f"Linear search O(n):")
    print(f" - Checks up to {num_courses} courses per search")
    print(f" - Time grows linearly with dataset size")
    print(f" - Average case: n/2 comparisons")
    print()
    print(f"Hash map lookup O(1):")
    print(f" - Direct index access in constant time")
    print(f" - Time remains constant regardless of dataset size")
    print(f" - Always 1 operation")
    print()
    print(f"With {num_courses} courses, hash map is ~{speedup:.1f}x faster")
    print(f"This advantage grows significantly with larger datasets")
    print()

    # projected scaling
    print("Projected Scaling")
    print("-" * 70)
    for scale in [10, 100, 1000, 10000]:
        scaled_courses = num_courses * scale
        print(f"With {scaled_courses:,} courses:")
        print(f" Linear search: ~{scaled_courses/2:,.0f} comparisons on average")
        print(f" Hash map:      1 operation (constant)")
        print()

    print("=" * 70)

def benchmark_validation():
    """ benchmark DFS cycle detection performance """

    print("=" * 70)
    print("DFS cycle detection performance")
    print("=" * 70)
    print()

    planner = CoursePlanner()
    csv_path = Path(__file__).parent.parent / 'data' / 'CS_300_ABCU_Advising_Program_Input.csv'
    planner.load_courses_from_csv(str(csv_path))

    num_courses = planner.get_course_count()

    print(f"dataset: {num_courses} courses")
    print("running validation with DFS cycle detection")
    print()

    start_time = time.perf_counter()
    is_valid, errors = planner.validate_prerequisites()
    elapsed = time.perf_counter() - start_time

    print(f"validation completed in: {elapsed*1000:.2f} milliseconds")
    print(f"result: {'Valid' if is_valid else 'Invalid'}")
    print(f"issues found: {len(errors)}")
    print()

    print("complexity analysis")
    print("-" * 70)
    print("DFS cycle detection: O(V + E)")
    print(f" V (vertices/courses): {num_courses}")
    print(f" E (edges/prerequisites): {sum(len(c.prerequisites) for c in planner.courses)}")
    print()
    print("DFS visits each course once then checks each prerequisite once,")
    print("making it fairly efficient for larger course catalogs")
    print()

if __name__ == "__main__":
    benchmark_search_methods(iterations=1000)
    print()
    benchmark_validation()