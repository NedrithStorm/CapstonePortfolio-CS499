import tkinter as tk
import Database
import Courses
import EDUgui

def main():
    #Make a database object and connect it
    db = Database.Database()
    db.connect_database("edu_db.db")
    #get initial course catalog from the DB
    course_catalog = Courses.Courses()
    for course_data in db.retrieve_all_courses():
        course = Courses.Course()
        course.course_id = course_data[0]
        course.course_name = course_data[1]
        course.prereqs = db.find_prereqs(course_data[0])
        course_catalog.insert_course(course)        

    #now that we have a catalog let's setup the gui first by making the root window
    root = tk.Tk()
    #Create a gui
    gui = EDUgui.EDUgui(root,db,course_catalog)
    #root2 = tk.Tk()

    #finally name it and loop
    root.title("Course Catalog")
    root.mainloop()

if __name__ == "__main__":
    main()