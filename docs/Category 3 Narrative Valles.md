## Artifact Description

The artifact that I chose for Enhancement 2 is Project Two from CS-300 – DSA: Analysis and Design which I had completed during the 2024 C-4 Term. The original artifact was a course planning application written in C++ using Visual Studio; it provides a menu-driven interface for managing course information. The program reads course data from a specific CSV file, stored it in a vector-based data structure, and allowed users to load course data, display a sorted list of all courses, and search for specific courses, with their prerequisites.

Another artifact chosen was Project 3 from CS-360 – Mobile Application Development. This served as a baseline and inspiration for the final enhancement of this project. Project 3 was an Android application built using Java and Android Studio, with a database section implemented via SQLite. The app is a weight tracking application, where there is a one-to-many table to represent the user and data entries made. With some minor changes, a similar format could be utilized to add database functionality to the overall project. 

This artifact in this enhancement specifically builds upon the improvements of the previous enhancement, which consisted of a conversion to a Python CLI tool with argparse and improved algorithmic computations. For persistence, pickle-based caching was used, but this has some issues as cache corruption could occur from program crashes, data corruption/migration, and was limited to Python in scope.

## Justification 

I mainly selected Project 3 from CS-360, specifically the DatabaseHelper.java file as it served an important role in data persistence for that project. Using CRUD operations and two tables within a one-to-many relationship, user data was stored as well as entries they made within the application. SQLite is a great format as it can be embedded into the device as a file, written in Java via modules within Android Studio. There were also proper practices being made, such as referencing foreign keys, and parameterized queries for secure data handling. 

These aspects served as a great foundation for adapting to the Course Planner project. Python has a native SQLite module, and an SQLite database gracefully implements true persistence within the application while still being lightweight and deployable everywhere. 

## Skills Demonstrated

Enhancement Three demonstrates multiple critical competencies required in software development:

**Database Design**

Normalized relational schema, proper use of primary and foreign keys, junction tables for many-to-many relationships, and strategic index placement for query optimization.

**Security Implementation**

Parameterized queries preventing SQL injection, input validation and sanitization, and secure transaction handling with automatic rollback.

**Transaction Management** 

Context managers for ACID compliance, proper connection lifecycle management, and error handling with graceful degradation.

**Data Migration**

ETL pipeline design (Extract from CSV, Transform data structures, Load to database), validation during migration, and comprehensive error reporting.

**API Design**

Clean DatabaseManager interface with logical method naming, comprehensive docstrings with complexity analysis, and separation of concerns between database operations and core logic.

## Course Outcomes

**Course Outcome 5: Develop a security mindset** 

Every database query within the enhancement, much like the artifact uses parameterized statements to prevent SQL injection attacks. This is especially important in cloud contexts, where this tool could potentially be used in internet or WAN settings. Input validation normalizes course numbers and filters empty strings before database insertion. Transaction isolation prevents race conditions in concurrent access scenarios. The security mindset is evident overall not just in the implementation, but also what we avoid using such as no string concatenation in SQL, no raw user input in queries, and no exception details being exposed to users.

## Reflection

**Learning Outcomes**

Enhancement Three overall was an exercise in deepening my understanding of database systems in a tangible setting. Implementing a production-ready database layer revealed the importance of details I had previously overlooked such as transaction isolation, connection lifecycle management, and the distinction between schema-level and application-level validation.

Putting myself in a security mindset forced me to focus on how I think about user input and why I made the decisions I made in the artifact that served as the foundation for this enhancement. Every string that enters the system is now a potential attack vector until proven safe. Parameterized queries aren't just industry best practice, as they're the minimum standard for responsible database programming. Input validation is acknowledging that users make mistakes as well as the fact that malicious behavior exists. This mindset shift will influence every database interaction I write going forward.

I also gained appreciation for the tradeoffs between different storage approaches. SQLite adds overhead such as connection management, transaction logic, and query parsing. These are aspects that pickle caching avoids which is something I hadn’t realized when initially implementing it back in Enhancement One. For this application with four courses, the performance difference is negligible. But the database provides guarantees pickle cannot: ACID compliance, query capabilities, concurrent access support, and tools for backup and replication. Understanding when these guarantees justify the complexity is crucial for architectural decisions.

**Challenges** 

***SQL Syntax Errors***

During initial schema creation, I encountered a syntax error near a closing parenthesis. The issue was subtle as I had an extra closing parenthesis after defining the updated\_at column with a default value. The SQL looked correct at first glance, but careful line-by-line inspection revealed the duplicate. This was a lesson learned in juggling multiple syntax paradigms and also considering editing first with SQL highlighting then factoring it into the Python code – something I recall doing back in CS-360 that I had forgotten about.

***Transaction Context Management*** 

Implementing proper transaction handling with automatic rollback requires understanding Python's context manager protocol. I implemented a transaction() method using the @contextmanager decorator that yields the connection, commits on successful exit, and rolls back on exceptions. This pattern ensures database consistency even when errors occur which is a critical feature for production systems that I hadn't fully appreciated in previous coursework. 

***Dual-Mode Architecture*** 

Supporting both CSV and database modes without code duplication requires careful interface design that I honestly didn’t plan that well for. Sometimes I would run into issues such as checking for the cache despite the program not knowing what type of persistence to use yet. I solved this by adding use\_database and db parameters to CoursePlanner's constructor, conditionally initializing a DatabaseManager instance. Methods like get\_course\_count() check use\_database and delegate to either self.courses (CSV mode) or self.db (database mode). This architecture maintains backward compatibility while cleanly separating the two backends.

