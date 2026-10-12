import unittest
from Edu_software import Course, Courses, Database
DB_NAME = "edu_db"
class TestCourses(unittest.TestCase):

    def test_insert_course(self):
        courses = Courses()

        course = Course()
        course.course_id = "CS101"
        course.course_name = "Introduction to Programming"

        courses.insert_course(course)

        self.assertEqual(len(courses.course_list), 1)
        self.assertEqual(courses.course_list[0].course_id, "CS101")

    def test_find_course(self):

        courses = Courses()

        course = Course()
        course.course_id = "CS101"
        course.course_name = "Introduction to Programming"

        courses.insert_course(course)

        result = courses.find_course("CS101")

        self.assertIsNotNone(result)
        self.assertEqual(result.course_id, "CS101")

    def test_course_not_existing(self):
        courses = Courses()

        course = Course()
        course.course_id = "CS101"
        course.course_name = "Introduction to Programming"

        courses.insert_course(course)

        result = courses.find_course("MATH101")

        self.assertIsNone(result)

    def test_validate_courses_success(self):
        courses = Courses()

        course = Course()
        course.course_id = "CS101"
        course.course_name = "Introduction to Programming"

        course2 = Course()
        course2.course_id = "CS200"
        course2.course_name = "Advanced Programming"
        course2.prereqs = ["CS101"]

        courses.insert_course(course)
        courses.insert_course(course2)

        self.assertEqual(courses.validate_all_courses(), [])

    def test_validate_courses_failure(self):

        courses = Courses()

        course = Course()
        course.course_id = "CS200"
        course.course_name = "Advanced Programming"
        course.prereqs = ["CS101"]

        courses.insert_course(course)

        self.assertEqual(len(courses.validate_all_courses()), 1)

    def test_database_create_course(self):

        db = Database()
        db.connect_database(DB_NAME)
        db.create_course("CS101","Introduction to CS")
        course = db.find_course("CS101")

        self.assertEqual("CS101",course[0])
        self.assertEqual("Introduction to CS",course[1])

    def test_database_delete_course(self):
        
        db = Database()
        db.connect_database(DB_NAME)
        db.create_course("CS101","Introduction to CS")
        course = db.find_course("CS101")

        self.assertEqual("CS101",course[0])

        db.delete_course("CS101")

        course = db.find_course("CS101")

        self.assertIsNone(course)
    
if __name__ == "__main__":
    unittest.main()
