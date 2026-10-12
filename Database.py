import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.dbName = ""

    def create_database(self):
        if self.conn is not None:
            cursor = self.conn.cursor()

            cursor.execute('''
             CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL
                )

            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS courseprereq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id TEXT NOT NULL,
                prereq TEXT NOT NULL,
                UNIQUE(course_id, prereq))  
            ''')

            self.conn.commit()
    def create_course(self,course_id,course_name):
        if self.conn is not None:
            cursor = self.conn.cursor()
            new_course = (course_id,course_name)
            course = self.find_course(course_id)
            if course is None:
                cursor.execute("INSERT INTO courses (course_id,course_name) VALUES (?, ?)", new_course)
                self.conn.commit()

                return cursor.rowcount == 1

        return False

    def delete_course(self,course_id):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM courseprereq WHERE course_id = ?",(course_id,))
            cursor.execute("DELETE FROM courseprereq WHERE prereq = ?",(course_id,))
            cursor.execute("DELETE FROM courses WHERE course_id = ?",(course_id,))

            self.conn.commit()

            return cursor.rowcount == 1

    def delete_prereq(self,course_id,prereq_id):
        if self.conn is None:
            return False

        cursor = self.conn.cursor()

        cursor.execute(
            """DELETE FROM courseprereq WHERE course_id = ? AND prereq = ?""",
            (course_id, prereq_id)
        )

        self.conn.commit()

        return cursor.rowcount == 1
    
    def find_course(self, course_id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id, ))
        result = cursor.fetchone()

        if result:
            return result
        else:
            return None

    def connect_database(self, db_name):
            self.conn = sqlite3.connect(db_name)
            self.create_database()

    def retrieve_all_courses(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM courses ORDER BY course_id ASC")

        return cursor.fetchall()

    def add_prereq(self,course,prereq):

        if self.find_course(course) is not None:
            if self.find_course(prereq) is not None:
                if prereq not in self.find_prereqs(course):
                    cursor = self.conn.cursor()
                    data = (course,prereq)
                    cursor.execute("INSERT INTO courseprereq (course_id,prereq) VALUES (?, ?)", data)
                    self.conn.commit()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def find_prereqs(self, course):
        if self.conn is None:
            return []
        
        if self.find_course(course) is None:
            return []
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT prereq
            FROM courseprereq
            WHERE course_id = ?
            """, (course, ))

        prereqs = [row[0] for row in cursor.fetchall()]

        return prereqs

    def update_course(self,course_id,course_name):
        if self.conn is not None:
            cursor = self.conn.cursor()

            cursor.execute(
                "UPDATE courses SET course_name = ? WHERE course_id = ?",
                (course_name, course_id)
            )

            self.conn.commit()

            return cursor.rowcount == 1