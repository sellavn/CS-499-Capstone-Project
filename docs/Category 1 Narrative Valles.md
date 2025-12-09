## Artifact Description

The artifact that I chose for Enhancement 1 is Project Two from CS-300 – DSA: Analysis and Design which I had completed during the 2024 C-4 Term. The original artifact was a course planning application written in C++ using Visual Studio; it provides a menu-driven interface for managing course information. The program reads course data from a specific CSV file, stored it in a vector-based data structure, and allowed users to load course data, display a sorted list of all courses, and search for specific courses, with their prerequisites.

Some more technical details of the application are that it consists of roughly 200 lines of C++ code organized into a Course struct for data storage and a CoursePlanner class that handles file I/O, data management, and user interaction through a text-based menu loop from a binary. While functional for its original purpose, the program had several limitations. These consist of things such as hardcoded values, monolithic class design, and simple data persistence.  

## Justification 

I selected this artifact for enhancement since it provided a clean foundation for demonstrating software engineering practices and modern development techniques. The original implementation is functional, but it can be improved to be an example of how I would create a production ready tool for my career of interest in infrastructure. 

## Skills Demonstrated

**Modern Python Dev Practices**

In this enhancement, I implemented modern Python 3.x best practices that are essential in today’s software industry. I implemented dataclasses with the @dataclass decorator to create clean, self-documenting data structures that automatically generate initialization and string representation methods, reducing boilerplate code while improving readability. Throughout the codebase, I incorporated comprehensive type hints on function parameters and return values. These values provide static type checking capabilities as well as serving as inline documentation within the codebase. Each function and class includes docstrings that follow Python conventions, explain parameters, return values and exceptions. These are modern Python software development practices that prioritize maintainability, collaboration, and functionality.

**CLI Tool Development**

Instead of a direct C++ to Python port, I decided to make it a more plausible context by creating a CLI using argparse. This new design implements subcommands similar to most other professional CLI tools like git or docker, where each command has its own documentation, arguments, and validation. The architecture is more intuitive for users familiar with modern CLI tools and allows the application to be integrated into those workflows that require aspects of scripting and automation. This made me think beyond basic functionality and consider who the end user is and how they utilize tools in this context of a CLI, specifically infrastructure workflows.

**Configuration Management and Separation of Concerns**

One foundation for a significant improvement is implementing external configuration management through a dedicated ConfigManager class that reads from a config.ini. This is one of the mitigations created to address where the CSV filename was hardcoded into the class directly. The new design allows users to modify default behaviors without touching the source code, making the application more flexible for different deployment scenarios. The configuration system also provides defaults if the config file is missing, which is an example of defensive programming. This enhancement showcases my understanding of configurable and maintainable software for users who may not have access to or the ability to edit the source code.

**Modularity**

The enhanced version restructures the monolithic design of the original into a cleaner and modular architecture that is well documented and expresses a clear separation of concerns:

- Models.py for data structures

- Course\_planner.py for business logic

- Cli.py for the user interface

- Config\_manager.py for configuration

- Init.py for initialization

- Main.py for the module entry point


Each module is made to be maintainable, well documented, and independently debuggable. This approach demonstrates my understanding that professional software must be designed for long-term maintainability from the start rather than initial functionality.

**Data Persistence and Cross-platform compatibility**

After the first couple of iterations, despite ample planning via flowcharts, pseudocode and a code review, I had an oversight in my design that led to my realization that the project would not work without some sort of persistence at play. Without it, the program would have needed a different approach. 

Persistence was achieved via the Pickle module, a native caching module in Python. After loading course data, the application stores it in a cache file, course\_cache.pkl, which allows subsequent commands to access the data cleanly. The feature also inadvertently addresses a limitation the previous program had, which was that it lacked any persistence. The use of pathlib for all file operations ensures cross-platform compatibility across Windows, macOS and Linux. 

## Course Outcomes

**Course Outcome 2: Design, develop, and deliver professional-quality oral, written, and visual communications**

I believe this is one of the stronger outcomes in this enhancement in various aspects. To start, the comprehensive docstrings throughout the codebase serve as self-documenting code that communicate design decisions, usage, and even future implementation plans to other developers. Type hints further the usage of self-documenting code and predictability by providing clear contracts for function interfaces without requiring further external documentation. The usage of argparse enables further documentation through the –-help command. In terms of the design of the codebase, the modular structure serves as an indication of the specific functionality of each aspect of the program, further detailed and visualized within the README. The README file is detailed and adapted for various audiences such as end user and developer alike. This demonstrates my ability to write technical documentation to describe the project at hand.

**Course Outcome 4: Demonstrate an ability to use well-founded and innovative techniques, skills, and tools in computing practices**

This outcome was achieved through the application of industry-standard tools and patterns. The argparse library represents the standard approach for CLI development in Python, used in countless professional tools. The pickle module for caching demonstrates understanding of serialization techniques for data persistence. The configparser module implements the widely used INI file format for basic configuration management. Dataclasses show my awareness of modern Python features that reduce boilerplate while improving overall code quality. The pathlib module demonstrates modern practices for cross-platform development. All tools are native Python modules, but in case non-standard modules are added, the requirements.txt is in place in case which follows best practice. Beyond specific tools, the overall architecture follows established software engineering principles like separation of concerns and modular design. These are well-known industry practices that demonstrate professional software development capability in the context of infrastructure roles.

## Reflection

**Learning Outcomes**

This was the first project in a long time where I had to think critically about how I would implement a professional grade tool, and the first time I had to make the requirements and outcomes myself. I read through a lot of documentation such as the PIP style guide, articles for each module used, and what are the best uses for them in the context I’m working in. The original C++ program functioned correctly as it loaded data, displayed courses, and handled searches. What the original artifact lacked were the architectural considerations that make software maintainable, mainly in terms of layout and documentation. This enhancement had me constantly thinking about how other developers could understand and modify this program, as well as how it could fit into a workflow.

A particular lesson learned was the need to implement persistence through caching. I didn’t realize that argparse was effectively a self-contained session, meaning that data had to be loaded, sorted and printed all at once. This was obviously not how I pictured the program working in the pseudocode, and I didn’t want to use something like an interactive session to achieve that, hence the need for persistence. This showed that I had a misunderstanding of how CLI tools work; users expect to run commands without repeatedly initializing them. The pickle-based caching emerged from both research and thinking about how a persistent session could be achieved in a professional manner.

Working with Python's type hints and dataclasses taught me about the extensibility of programming language features. Having learned mostly standard Python features in IT-140, when I first learned about type hints and dataclasses, it took me a while to realize the importance of the role they play in terms of error prevention and predictability. I noticed VSCodium giving me significantly improved autocomplete and error checking with type hints present, for example. This experience showed me that most programming languages have so many features that we don’t even touch in coursework, and that it is important to continually improve as the ecosystem grows and evolves over time.

**Challenges** 

***Data Persistence Architecture Decision***

As mentioned before, data persistence was a massive oversight that was unplanned for in the enhancement. The original C++ program ran a continuous process with a menu loop; data naturally persisted in memory though, so it wasn’t an issue. But doing a direct port of this functionality with argparse showed me this isn’t quite how CLI tools work. Each command is generally a separate process invocation, I thought about maintaining the continuous loop model via an interactive mode, but that didn’t really feel like a proper CLI tool to me. After research and some thinking, pickle-based cache ended up serving a proper middle ground, at least until Enhancement Three which would upgrade the persistence to be handled via SQLite when that becomes the focus. This decision required a lot of research and taught about making potentially project altering choices based on current scope and requirements, while still considering future iterations.

***Error Handling***

Determining the appropriate level of error handling was something I was a little unfamiliar with. I understood that too little error handling could result in the program crashing ungracefully, while too much and the code ends up becoming riddled with edge cases. I had to sort of mentally adjust for errors that users can address, such as a file not being found or issues with permissions, and errors that indicate programming bugs. How I ended up approaching it is user addressable errors receive clear, actionable messages, while unexpected errors print the exception details in verbose mode but provide a generic message to normal users. This approach maintains clean code while ensuring appropriate information reaches the right audience. I know that this can also be further expanded if I get around to adding logging. Overall, the process of creating error messages taught me that error handling is another facet of the user experience that I often don’t think about that a developer must consider.