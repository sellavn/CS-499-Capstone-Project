## Artifact Description

The artifact that I chose for Enhancement 2 is Project Two from CS-300 – DSA: Analysis and Design which I had completed during the 2024 C-4 Term. The original artifact was a course planning application written in C++ using Visual Studio; it provides a menu-driven interface for managing course information. The program reads course data from a specific CSV file, stored it in a vector-based data structure, and allowed users to load course data, display a sorted list of all courses, and search for specific courses, with their prerequisites.

This artifact in this enhancement specifically builds upon the improvements of the previous enhancement, which consisted of a conversion to a Python CLI tool with argparse. The original implementation, while functional, had limitations in the form of O(n) time complexity for search operations, meaning search time grew linearly with the number of courses. Enhancement Two, I have refactored this system with Python's dictionary data structures to create a hash map index that provides O(1) constant-time lookups regardless of dataset size.

## Justification 

I selected this artifact for enhancement since it provided a clean foundation for demonstrating software engineering practices and modern development techniques. By adding to my previous enhancement, I gained the opportunity to showcase more improvements in broader facets of software engineering. In this enhancement, I chose to focus primarily on the algorithmic shortcomings of the base artifact and previous enhancement. 

The original C++ implementation with its linear search approach is bound to be increasingly inefficient if used in a production setting. Let’s take a scenario where a course catalog within a university with 1,000 courses would require an average of 500 comparisons per search. By implementing hash map indexing, I reduce this to a single operation, regardless of catalog size. This dramatic improvement, measurable through performance benchmarking, provides concrete evidence of the practical value of algorithm selection and data structure design.

## Skills Demonstrated

**Algorithmic Understanding**

The implementation of the enhancement required a deep understanding of time and space complexity through the implementation of hash map indexing and the associated O(1) performance characteristics. Another aspect of this is shown in the proficiency of graph algorithms through the DFS cycle detection implementation, which treats courses and prerequisites as a directed graph and traverses it efficiently. Lastly, I needed analysis skills through performance benchmarking that empirically validates complexity predictions.

Trade off decisions were also made; the hash map requires O(n) additional space, but as a result provides dramatic time complexity improvements that justify this cost. Decisions like these must always be made in an infrastructure setting, and informed decisions can save costs and development time.

## Course Outcomes

**Course Outcome 3: Design and evaluate computing solutions that solve a given problem using algorithmic principles**

Enhancement 2 is centered around Course Outcome 3 for a variety of reasons. The performance benchmarks comparing O(n) versus O(1) search operations, as well as documentation of where the enhancements were, within the docstrings and code comments help paint a valid justification for why these design decisions were made. The enhancements were made precisely with minimal refactoring, and with a clear goal in mind. The DFS algorithms implementation for cycle detection has detailed state tracking, and the manual validation command gives the end user assurance. The goal of this enhancement was to demonstrate an applicable use of algorithms and be able to practically implement, test, and validate the improvements in the context of CLI software, which could be used in the context of infrastructure roles.

## Reflection

**Learning Outcomes**

I had a lot of anxiety and prepared a lot going into Enhancement Two of the broader Capstone project. While I had an adequate grasp of data structures and algorithmic complexity, this was the first time I had thought about it in a personal project of mine. I reflected on my time in my DSA class, where this original artifact was from, as well as any other examples of DSA principles I have encountered in previous coursework. Ultimately, thorough planning, research, and review helped ease the tension greatly. Planning for the direct improvement using Big O notation in the context of this artifact and furthermore illustrated by the benchmark I created made the concepts significantly more tangible, and less daunting to implement. 

Once the benchmark was completed and run, the results showed that the hash map was consistently faster even with the tiny dataset used. This means the hypothetical scenario mentioned in the justification section earlier would benefit greatly from the improvements made in this enhancement.

I felt implementing the DFS cycle detection algorithm taught me the value of careful state management in recursive algorithms. The three-set approach (visited, in\_progress, reported\_cycles) elegantly solves multiple problems simultaneously, preventing infinite recursion, avoiding redundant traversals, and foregoing duplicate error reporting. The experience of implementing the improvements for these enhancements reinforced the importance of thoughtful data structure selection and realistic targeted optimization.

**Challenges** 

***Infinite Recursions*** 

The most significant challenge was implementing cycle detection without falling into infinite recursions, which happened more times than I would like to admit. Multiple of my initial iterations of the DFS implementation would loop indefinitely when encountering circular dependencies because it continued recursing even after detecting a cycle. I solved this by implementing proper early termination. When a cycle is detected, the function immediately returns, which prevents further recursion in that path. Additionally, I had to manage the ‘in\_progress’ set carefully, adding courses when entering their DFS calls and removing them when exiting, ensuring the set accurately represents the current recursion path.

***Cycle Reports***

Another issue was with duplicate cycle reports. A circular dependency between courses A and B would be detected twice, once when traversing from A to B, and again with traversing from B to A. I ended up solving this by implementing a ‘reported\_cycles’ set that stores normalized cycle pairs, which are sorted tuples of course numbers. Before reporting a cycle, the algorithm checks if it had already been reported, ensuring each circular dependency appears only once in the error output.