/*
CS-300 Project Two - ABCU Scheduling Application
Nick Valles
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// Structure to store course information
struct Course {
    string courseNumber;
    string name;
    vector<string> prerequisites;
};

// trim from start (in place)
static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !std::isspace(ch);
    }));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
    ltrim(s);
    rtrim(s);
}

// Class to handle course planning
class CoursePlanner {
private:
    vector<Course> courses; // Vector to store all courses
    const string filename = "CS 300 ABCU_Advising_Program_Input.csv"; // CSV file name

    // Function to read and validate the CSV file
    bool ReadAndValidateFile();
    // Function to print course information
    void PrintCourseInfo(const string& searchCourseNumber) const;
    // Function to print a sorted list of courses
    void PrintSortedCourseList() const;

    // Function to convert a string to uppercase and trim it
    string toUpper(string s) const {
        trim(s); // Trim the string
        transform(s.begin(), s.end(), s.begin(), [](unsigned char c) { return toupper(c); });
        return s;
    }

public:
    // Function to load the data structure from the CSV file
    bool LoadDataStructure();
    // Function to run the course planner application
    void Run();
};

// Function to read and validate the CSV file
bool CoursePlanner::ReadAndValidateFile() {
    ifstream file(filename); // Open the file
    if (!file) { // Check if the file opened successfully
        cout << "Error: File not found" << endl;
        return false;
    }

    courses.clear(); // Clear the courses vector
    string line;
    while (getline(file, line)) { // Read each line from the file
        vector<string> fields;
        size_t pos = 0;
        while ((pos = line.find(',')) != string::npos) { // Split line by commas
            fields.push_back(line.substr(0, pos));
            line.erase(0, pos + 1);
        }
        fields.push_back(line); // Add the last field

        if (fields.size() < 2) { // Check for valid line format
            cout << "Error: Invalid line format" << endl;
            continue;
        }

        Course course; // Create a new course
        course.courseNumber = toUpper(fields[0]); // Convert course number to uppercase and trim it
        course.name = fields[1]; // Set the course name
        course.prerequisites = vector<string>(fields.begin() + 2, fields.end()); // Set the prerequisites

        // Remove any empty prerequisites
        course.prerequisites.erase(
            remove_if(course.prerequisites.begin(), course.prerequisites.end(), [](const string& s) { return s.empty(); }),
            course.prerequisites.end());

        courses.push_back(course); // Add the course to the courses vector
    }

    file.close(); // Close the file

    

    return true;
}

// Function to print course information
void CoursePlanner::PrintCourseInfo(const string& searchCourseNumber) const {
    string upperSearchCourseNumber = toUpper(searchCourseNumber); // Convert search course number to uppercase and trim it
    for (const auto& course : courses) { // Iterate through all courses
        if (course.courseNumber == upperSearchCourseNumber) { // Check if course number matches
            cout << course.courseNumber << ", " << course.name << endl; // Print course number and name
            if (course.prerequisites.empty()) { // Check if there are no prerequisites
                cout << "Prerequisites: None" << endl;
            } else { // Print prerequisites
                cout << "Prerequisites: ";
                for (size_t i = 0; i < course.prerequisites.size(); ++i) {
                    cout << course.prerequisites[i];
                    if (i < course.prerequisites.size() - 1) {
                        cout << ", ";
                    }
                }
                cout << endl;
            }
            return;
        }
    }
    cout << "Course not found" << endl; // Print message if course is not found
}

// Function to print a sorted list of courses
void CoursePlanner::PrintSortedCourseList() const {
    vector<Course> sortedCourses = courses; // Copy the courses vector
    sort(sortedCourses.begin(), sortedCourses.end(), [](const Course& a, const Course& b) { return a.courseNumber < b.courseNumber; }); // Sort courses by course number

    cout << "Here is a sample schedule:" << endl;
    for (const auto& course : sortedCourses) { // Print all courses
        cout << course.courseNumber << ", " << course.name << endl;
    }
}

// Function to load the data structure from the CSV file
bool CoursePlanner::LoadDataStructure() {
    return ReadAndValidateFile();
}

// Function to run the course planner application
void CoursePlanner::Run() {
    cout << "Welcome to the course planner." << endl;

    while (true) {
        cout << "1. Load Data Structure." << endl;
        cout << "2. Print Course List." << endl;
        cout << "3. Print Course." << endl;
        cout << "9. Exit" << endl;
        cout << "What would you like to do? ";

        int choice;
        cin >> choice; // Get user choice

        switch (choice) {
            case 1:
                if (LoadDataStructure()) { // Load data structure
                    cout << "Data loaded successfully." << endl;
                } else {
                    cout << "Failed to load data." << endl;
                }
                break;
            case 2:
                if (courses.empty()) { // Check if courses vector is empty
                    cout << "Please load the data first." << endl;
                } else {
                    PrintSortedCourseList(); // Print sorted course list
                }
                break;
            case 3:
                if (courses.empty()) { // Check if courses vector is empty
                    cout << "Please load the data first." << endl;
                } else {
                    string courseNumber;
                    cout << "What course do you want to know about? ";
                    cin >> courseNumber; // Get course number from user
                    PrintCourseInfo(courseNumber); // Print course information
                }
                break;
            case 9:
                cout << "Thank you for using the course planner!" << endl;
                return; // Exit the program
            default:
                cout << choice << " is not a valid option." << endl; // Invalid choice message
        }

        cout << endl;
    }
}

int main() {
    CoursePlanner planner;
    planner.Run(); // Run the course planner application
    return 0;
}
