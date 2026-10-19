import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.dbName = ""
    """Creates a new database"""
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

    """Creates a course with given course_id and name
    
        Returns:
            Trues if course created, false otherwise
            
    """
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
    """Deletes a course
    
        Args:
            course_id: id of course to delete
            
        Returns:
            True if course deleted, false otherwise
            
    """
    def delete_course(self,course_id):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM courseprereq WHERE course_id = ?",(course_id,))
            cursor.execute("DELETE FROM courseprereq WHERE prereq = ?",(course_id,))
            cursor.execute("DELETE FROM courses WHERE course_id = ?",(course_id,))

            self.conn.commit()

            return cursor.rowcount == 1
    """Deletes a pre-req from a course
    
        Args:
            course_id: course to remove prereq from
            prereq_id: course id of pre-req to remove
            
        Returns:
            True if prereq add, false otherwise
            
    """
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
    """finds a course with the given course_id
    
        Args:
            course_id: course to find
            
        Return:
            course found
            
    """
    def find_course(self, course_id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id, ))
        result = cursor.fetchone()

        if result:
            return result
        else:
            return None
    """connects to a database with a given name"""
    def connect_database(self, db_name):
            self.conn = sqlite3.connect(db_name)
            self.create_database()
    """Returns a list of all courses"""
    def retrieve_all_courses(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM courses ORDER BY course_id ASC")

        return cursor.fetchall()
    """Adds a prereq to a course
    
        Args:
            course: course to add prereq to
            prereq: prereq of course to add
            
        Returns:
            True if prereq added, false otherwise
            
    """
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
    """finds all pre-reqs for a given course
    
        Args:
            course: course id to find prereqs
            
        Returns:
            array of prereqs for the course, empty array if none exists
            
    """
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
    """Updates a course's name
    
        Args:
            course_id: course_id to update
            course_name: new name of the course
            
        Returns:
            True if course updated, false otherwise
            
    """
    def update_course(self,course_id,course_name):
        if self.conn is not None:
            cursor = self.conn.cursor()

            cursor.execute(
                "UPDATE courses SET course_name = ? WHERE course_id = ?",
                (course_name, course_id)
            )

            self.conn.commit()

            return cursor.rowcount == 1