#a Single course
class Course:
    def __init__(self):
        self.course_id = "none"
        self.course_name = ""
        self.prereqs = []
#A group of courses
class Courses:
    def __init__(self):
        self.course_list = []
        self.course_table = {}
        #when an item is inserted, the list is considered unsorted
        self.sorted = True

    def validate_all_courses(self):
        """Validates the course catalog to ensure that all pre-reqs exist in the catalog
        
        Returns:
            An array of errors or an empty array for no errors
        """
        #create a set of all course ids
        course_ids = set()
        errors = []
        #for every course, check to see if it already exists in the set, create error if it does otherwise add itk
        for course in self.course_list:
            if course.course_id in course_ids:
                errors.append(
                    f"Duplicate Course ID found: {course.course_id}"
                )
            else:
                course_ids.add(course.course_id)


        #for every course, examine it's prereqs
        for course in self.course_list:
            for prereq in course.prereqs:
                #if the prereq doesn't exist in the set then the catalog isn't valid.  Add the bad prereq to the error array
                if prereq not in course_ids:
                    errors.append(
                        f"{course.course_id}: prerequisite {prereq} does not exist"
                    )
        return errors

    def find_course(self, course_id, hash = True):
        """Finds the course that has the given course_id

        Args:
            course_id: course_id to find

        Returns:
            course class of course found, None if nothing was found

        
        """
        if hash:
            if course_id in self.course_table:
                return self.course_table[course_id]
            else:
                return None
        #if not sorted, sort
        if not self.sorted:
            self.sort_courses()
        #search entire list
        low = 0
        high = len(self.course_list) - 1
        # while the course could still be found
        while low <= high:
            #midway point search
            mid = (low + high) //2

            current_id = self.course_list[mid].course_id
            #if found return it otherwise set the new low or high point based on findings
            if(current_id == course_id):
                return self.course_list[mid]
            elif current_id < course_id:
                low = mid + 1
            else:
                high = mid - 1

        return None

    def print_course(self, course, print_prereqs=False):
        """ returns a nice looking output string

        Args:
            course: course to print
            print_prereqs: Whether or not to returnthe pre-reqs

        Returns:
            A formated output string 
        """
        output = (
            f"Course ID: {course.course_id}\n"
            f"Course Name: {course.course_name}\n"
        ) 

        if course.prereqs and print_prereqs:
            output += "Prerequisites: " + ", ".join(course.prereqs)
        elif not course.prereqs:
            output += "Prerequisites: None"
        return output

    def insert_course(self, course):
        """Insert given course to catalog and set list to unsorted"""
        self.course_list.append(course)
        self.course_table[course.course_id] = course
        self.sorted = False

    def delete_course(self, course_id):

        course = self.find_course(course_id)

        if course is None:
            return False
        
        self.course_list.remove(course)
        self.course_table.pop(course_id)

        return True

    def delete_prereq(self,course_id,prereq_id):
        course = self.find_course(course_id)

        if course is None:
            return False

        if prereq_id not in course.prereqs:
            return False

        course.prereqs.remove(prereq_id)

        return True
    def remove_prereq_from_courses(self, prereq_id):
         for course in self.course_table.values():
            if prereq_id in course.prereqs:
                course.prereqs.remove(prereq_id)
    
    def sort_courses(self):
        """Uses pythons built in sort function to sort the course catalog when needed"""
        if(self.sorted == False):
            self.course_list.sort(key=lambda course: course.course_id)
        self.sorted = True

    def get_number_of_courses(self):  
        """Returns the number of courses in the course catalog"""
        return len(self.course_list) 

    def add_pre_req(self, course_id, prereq_id):
        course = self.find_course(course_id)

        if course is None:
            return False

        if prereq_id in course.prereqs:
            return False

        if course_id == prereq_id:
            return False

        if prereq_id in course.prereqs:
            return False

        course.prereqs.append(prereq_id)
        return True