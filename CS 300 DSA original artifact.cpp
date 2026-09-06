//============================================================================
// Name        : Project2.cpp
// Author      : Andrew Good
// Version     : 1.0
// Copyright   : Copyright © 2023 SNHU COCE
// Description : Project 2 done using a vector to load and print a list of courses
//============================================================================
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
//============================================================================
// course structure and course list class - normally courses.h
//============================================================================

//a structure for each course
struct course {
	//defaulting courseId to none to identify a blank course
	string courseId = "none";
	string courseName = "";
	vector<string> preReqs;
};
//a class for courses
class courses {
private:
	vector<course> courseList;
	void quickSort(int low, int high);
	int partition(int low, int high);
	//when an item is inserted the coursesList is considered unsorted
	//only call quicksort when needed
	bool sorted;
public:
	courses() { sorted = true; }
	int binarySearch(string targetCourseId);
	void printAllCourses();
	string validateAllCourses();
	course findCourse(string courseSelection);
	void printCourse(course course, bool printPreReqs = false);
	void insertCourse(course course);
	void quickSort();
	int getNumberOfCourses();
};

//============================================================================
// function declarations
//============================================================================
void printMenu();
courses loadData(string fileName);
string parseItem(string& line);

/**
 * The one and only main() method
 */
int main() {
	int choice = 0;
	string fileName = "";
	string courseSelection = "";
	courses courseList;

	cout << "Welcome to the course planner." << endl;
	//while the choice isn't to exit
	while (choice != 9) {
		course singleCourse;
		//print menu and get choice
		printMenu();
		cin >> choice;
		switch (choice) {
			//load data
		case 1:
			//get file name
			cout << "What is the file containing the course list? ";
			cin >> fileName;
			//load data
			courseList = loadData(fileName);
			cout << endl;
			break;
			//print all courses
		case 2:
			//let the user know they haven't loaded course data yet
			if (courseList.getNumberOfCourses() == 0) {
				cout << "No course data loaded!" << endl << endl;
				break;
			}
			cout << "Here is a sample schedule" << endl << endl;
			courseList.printAllCourses();
			cout << endl;
			break;
			//print specific course
		case 3:
			//let the user know they haven't loaded course data yet
			if (courseList.getNumberOfCourses() == 0) {
				cout << "No course data loaded!" << endl << endl;
				break;
			}
			//get course
			cout << "What course do you want to know about? ";
			cin >> courseSelection;
			//find course
			singleCourse = courseList.findCourse(courseSelection);
			//if course exists print it otherwise not it doesn't exist
			if (singleCourse.courseId != "none") {
				courseList.printCourse(singleCourse, true);
			}
			else {
				cout << courseSelection << " not found." << endl;
			}
			cout << endl;
			break;
		//exit - just here so it doesn't follow default
		case 9:
			break;
		//invalid option
		default:
			cout << choice << " is not a valid option." << endl << endl;;
			break;
		}
	}
	cout << "Thank you for using the course planner";
	return 0;
}
//============================================================================
// Helper functions
//============================================================================
/**
 * Prints the menu
 */
void printMenu() {
	cout << "1. Load Data Structure." << endl;
	cout << "2. Print Course list." << endl;
	cout << "3. Print Course." << endl;
	cout << "9. Exit" << endl;
	cout << endl << "What would you like to do? ";
}
/**
 * Loads all the data from a CSV file given by filename into a vector and returns it
 * This function also validates the CSV file before returning it to ensure that every pre-req has a course
 * Returns the loaded data if valid otherwise returns an empty vector
 */
courses loadData(string fileName) {
	//variable declarations
	courses courseList;
	int lineNumber = 0;
	courses blankCourseList;
	string currentLine = "";
	string validation = "";
	//opens the file fileName
	ifstream courseFile(fileName);
	//if the file couldn't be opened state the error and return a blank vector
	if (!courseFile) {
		cout << fileName << " could not be opened for reading." << endl;
		return blankCourseList;
	}
	//while there is stuff to read read it all into currentLine
	while (getline(courseFile, currentLine)) {
		//for error purposes
		lineNumber++;
		course course;
		//get the first part of the CSV line and make it the course Id
		course.courseId = parseItem(currentLine);
		//if there is nothing left to read in the CSV line the data is invalid as there is no course name
		if (currentLine == "") {
			cout << "line #" << lineNumber << " containing: " << course.courseId << " is invalid. Load cannot be completed." << endl;
			return blankCourseList;
		}
		//next item goes in course name
		course.courseName = parseItem(currentLine);
		//until the CSV line is done being read every other item goes into preReq
		while (currentLine != "") {
			string preReq = parseItem(currentLine);
			if (preReq != "") {
				course.preReqs.push_back(preReq);
			}
		}
		//finally we have all the data for that course so add it to the vector before moving on to the next line
		courseList.insertCourse(course);

	}

	//validate the pre-reqs
	validation = courseList.validateAllCourses();
	//if it's not valid note which pre-req failed and return a blank course
	if (validation != "valid") {
		cout << "Data file contains invalid data: pre-req: " << endl
			<< validation << " exists as pre-req for a course but no course exists" << endl;
		return blankCourseList;
	}
	//we can finally close the file and return the completed vector
	courseFile.close();
	return courseList;
}
/*parseItem removes everything before the first comma from line and returns it
 *If there is no comma parseItem returns line and turns line blank
 */
string parseItem(string& line) {
	//find the comma
	int commaLocation = line.find(",");
	string item = "";
	//if the comma doesn't exist set item to line, line to nothing
	if (commaLocation == -1) {
		item = line;
		line = "";
	}
	//it comma exists, item becomes everything before the comma and line becomes everything after
	else {
		item = line.substr(0, commaLocation);
		line = line.substr(commaLocation + 1);
	}
	//return everything before the line
	return item;
}
//============================================================================
// Courses class functions implementation - normally courses.cpp
//============================================================================
/**
 * Returns a course object containing that has a matching course ID = courseSelection
 */
course courses::findCourse(string courseSelection) {
	quickSort();
	//get the index of the course
	int index = binarySearch(courseSelection);
	//if it exists return the course
	if (index != -1) {
		return courseList[index];
	}
	//otherwise return a blank course;
	course blankCourse;
	return blankCourse;
}
/**
 * Prints a course and if printPreReqs is true prints all the courses pre-reqs
 */
void courses::printCourse(course course, bool printPreReqs) {
	//print basic course information
	cout << course.courseId << ", " << course.courseName << endl;
	//if we wanted to print prereqs and if some exist
	if (printPreReqs && course.preReqs.size() > 0) {
		cout << "Prerequisites: ";
		//for every prereq
		for (int i = 0; i < course.preReqs.size(); i++) {
			//print it out
			cout << course.preReqs[i];
			//if it's not the last one print a comma, if it is the last one a new line
			if (i != course.preReqs.size() - 1) {
				cout << ", ";
			}
			else {
				cout << endl;
			}
		}
	}
}
/**
 * Prints every single course without listing the pre-reqs
 */
void courses::printAllCourses() {
	//let's not waste time sorting an already sorted vector
	quickSort();
	//for each course print it
	for (course course : courseList) {
		printCourse(course);
	}
}

/**
 * Validates that all pre-reqs have a matching course
 * Returns the pre-req that first failed the validation if it fails otherwise returns "valid"
 */
string courses::validateAllCourses() {
	quickSort();
	//for each course
	for (course currentCourse : courseList) {
		//for each pre-req
		for (string preReq : currentCourse.preReqs) {
			//search the pre-req for a matching course and if not found return the pre-req indicating failure
			if (binarySearch(preReq) == -1) {
				return preReq;
			}
		}
	}
	//otherwise return a string indicating valid data
	return "valid";
}


/**
 * Quicksorts an entire vector from beginning to end
 */
void courses::quickSort() {
	//call quicksort to sort the entire vector
	if (isSorted) {
		return;
	}
	quickSort(0, courseList.size() - 1);
	sorted = true;
}
/**
 * Recursive quick sort, sorts the vector from low to high
 */
void courses::quickSort(int low, int high) {
	//if we aren't done
	if (low < high) {
		//sort using partition and get the pivot point
		int pivot = partition(low, high);
		//sort everything before the pivot point
		quickSort(low, pivot - 1);
		//sort everything after the pivot point
		quickSort(pivot + 1, high);
	}
}
/**
 * Creates a Pivot point at courses[high].  sorts the vector so that everything before the pivot point will be lower and everything after will be higher
 * Returns the new index for the pivot point
 */
int courses::partition(int low, int high) {
	//pivot is the item that is in the highest index
	string pivot = courseList[high].courseId;
	//index one below the low
	int index = low - 1;
	//from low to high

	for (int i = low; i < high; i++) {
		//if current item < pivot
		if (courseList[i].courseId < pivot) {
			//increase the index and then swap the indexed value with the current item
			index++;
			swap(courseList[index], courseList[i]);
		}
	}

	//finally the pivot should be at one after the index
	swap(courseList[index + 1], courseList[high]);
	//return the pivot point
	return index + 1;
}
/**
 * standard binary tries to find targetCourseId at the mid point then does the midpoint of the left or right section and continues until it finds target
 * returns the index of the first matching item
 */
int courses::binarySearch(string targetCourseId) {
	int low = 0;
	int high = courseList.size() - 1;
	int index = -1;
	while (index == -1) {
		if (high < low) {
			return -1;
		}
		int mid = (low + high) / 2;
		if (courseList[mid].courseId < targetCourseId) {
			low = mid + 1;
		}
		else if (courseList[mid].courseId > targetCourseId) {
			high = mid - 1;
		}
		else {
			return mid;
		}
	}
}
/**
 * Inserts a course into the class's courseList vector and marks the vector for sorting later
 */
void courses::insertCourse(course course) {
	courseList.push_back(course);
	//whenever we insert a course the vector is no longer considred sorted
	sorted = false;
}
/**
 * Returns the number of courses contained in the courses vector
 */
int courses::getNumberOfCourses() {
	return courseList.size();
}