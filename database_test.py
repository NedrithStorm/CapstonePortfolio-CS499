import unittest
import sqlite3
import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database.Database()
        self.db.conn = sqlite3.connect(":memory:")
        self.db.create_database()

    def tearDown(self):
        if self.db.conn is not None:
            self.db.conn.close()

    def test_create_course(self):
        result = self.db.create_course(
            "CS101",
            "Introduction to CS"
        )

        self.assertTrue(result)

        course = self.db.find_course("CS101")

        self.assertIsNotNone(course)
        self.assertEqual(course[0],"CS101")
        self.assertEqual(course[1],"Introduction to CS")

    def test_create_duplicate_course(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        result = self.db.create_course(
            "CS101",
            "Introduction to CS2"
        )

        self.assertFalse(result)

    def test_find_course_not_found(self):
        result = self.db.find_course("CS232")

        self.assertIsNone(result)

    def test_retreive_all_courses(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        self.db.create_course(
            "CS102",
            "Introduction to CS2"
        )

        courses = self.db.retrieve_all_courses()

        self.assertEqual(len(courses),2)

    def test_add_prereq(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        self.db.create_course(
            "CS102",
            "Introduction to CS2"
        )

        result = self.db.add_prereq("CS102","CS101")
        
        self.assertTrue(result)

        prereqs= self.db.find_prereqs("CS102")

        self.assertIn("CS101", prereqs)

    def test_duplicate_prereq(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        self.db.create_course(
            "CS102",
            "Introduction to CS2"
        )
        self.db.add_prereq("CS102","CS101")
        result = self.db.add_prereq("CS102","CS101")

        
        self.assertFalse(result)

        prereqs= self.db.find_prereqs("CS102")

        self.assertIn("CS101", prereqs)

    def test_update_course(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        result = self.db.update_course(
            "CS101",
            "Introduction to CS2"
        )

        self.assertTrue(result)

        course = self.db.find_course("CS101")

        self.assertEqual(course[1],"Introduction to CS2")

    def test_update_course_does_not_exist(self):
        result = self.db.update_course(
            "CS999",
            "testCourse"
        )

        self.assertFalse(result)

    def test_delete_course(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )

        result = self.db.delete_course("CS101")

        self.assertTrue(result)

        self.assertIsNone(
            self.db.find_course("CS101")
        )

    def test_delete_course_removes_prereq(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        self.db.update_course(
            "CS102",
            "Introduction to CS2"
        )

        self.db.add_prereq("CS102", "CS101")

        self.db.delete_course("CS102")

        prereqs = self.db.find_prereqs("CS102")

        self.assertEqual(prereqs, [])

    def test_delete_course_removes_prereq_from_others(self):
        self.db.create_course(
            "CS101",
            "Introduction to CS"
        )
        self.db.update_course(
            "CS102",
            "Introduction to CS2"
        )

        self.db.add_prereq("CS102", "CS101")

        self.db.delete_course("CS101")

        prereqs = self.db.find_prereqs("CS102")

        self.assertEqual(prereqs, [])

        cursor = self.db.conn.cursor()

        cursor.execute(
            "SELECT * FROM courseprereq WHERE prereq = ?",
            ("CS101",)
        )

        self.assertIsNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()