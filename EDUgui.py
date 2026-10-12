import tkinter as tk
from tkinter import ttk
import Courses
class EDUgui:
    def __init__(self,root,db,course_catalog):
        self.root = root
        self.db = db
        self.course_catalog = course_catalog

        self.catalog_tree = None
        self.course_information_text = None
        self.insert_type_box = None
        self.course_find_edit_box = None

        self.create_widgets()
    """Creates all of the widgets required for teh GUI"""
    def create_widgets(self):
        fram = tk.Frame(self.root)

        tk.Label(fram,text="Course to Find: ").pack(side = tk.LEFT)

        #create us an edit box and allow it to respond to the return key as a user would expect
        self.course_find_edit_box = tk.Entry(fram)

        self.course_find_edit_box.pack(side=tk.LEFT, fill=tk.BOTH, expand = 1)

        self.course_find_edit_box.focus_set()

        self.course_find_edit_box.bind("<Return>", 
                                lambda event: self.find_course_button(
                
                                ))

        #create a button to find the course
        find_course_button = tk.Button(fram, 
                        text = 'Find Course', 
                        command =lambda: self.find_course_button(

                        )
        )
        find_course_button.pack(side = tk.RIGHT)

        fram.pack(side=tk.TOP)
        bottom_bar_frame = tk.Frame(self.root)
        bottom_bar_frame.pack(side=tk.BOTTOM,pady=20)
        #create a drop-down box
        options = ["Course","Pre-req"]
        self.insert_type_box = ttk.Combobox(
            bottom_bar_frame, 
            values=options,
            state="readonly"
        )

        self.insert_type_box.pack(padx = 20, side=tk.LEFT)
        self.insert_type_box.current(0)
        
        #create a delete button
        self.delete_button = tk.Button(
            bottom_bar_frame, 
            text = 'Delete Item', 
            command =lambda: self.delete_selected_item(
            )
        )
        self.delete_button.pack(padx = 10, side=tk.RIGHT)

        #create an insert button
        self.insert_item_button = tk.Button(bottom_bar_frame, 
                        text = 'Insert Item', 
                        command =lambda: self.add_item(
                        )
        )
        self.insert_item_button.pack(side=tk.RIGHT)

        #create an update button
        self.update_course_button = tk.Button(bottom_bar_frame,
                        text = 'Update Selected',
                        command = lambda: self.edit_course_form()                      
                        )
        self.update_course_button.pack(side=tk.RIGHT)

        self.course_information_text = tk.Text(self.root, height = 8)
    #this box will be used to display individual searched for courses.
        self.course_information_text.insert('1.0','''''')
        self.course_information_text.pack(side=tk.BOTTOM)
        
        #now we want to create a frame for the list of courses
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill = "both", expand = True)

    #and a scroll bar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill= "y")

    #putting it all together
        self.catalog_tree = ttk.Treeview(
                            tree_frame, 
                            columns=("ID", "Name"), 
                            show = "headings",
                            yscrollcommand=tree_scroll.set
                            )

        self.catalog_tree.bind("<<TreeviewSelect>>", 
                      lambda event: self.select_tree_row(
                        event

    ))
    #ensure the tree reacts to the scroll bar
        tree_scroll.config(command=self.catalog_tree.yview)

    #setup the table with heading labels and widths
        self.catalog_tree.heading("ID", text = "Course ID")
        self.catalog_tree.heading("Name", text = "Course Name")

        self.catalog_tree.column("ID", width = 100)
        self.catalog_tree.column("Name", width = 300)

        self.catalog_tree.pack(fill="both", expand=True)

    #now let's insert the information into each cell of the tree frame
        for course in self.course_catalog.course_list:
                self.catalog_tree.insert(
                "",
                tk.END,
                iid=course.course_id,
                values=(course.course_id,course.course_name)
            )




        #create a text box before the edit box to explain it

    """Gets the text from the find course field if found prints the course into the course information field """
    def find_course_button(self):
    #get the text from the course_find_edit_box field
        course_id = self.course_find_edit_box.get()
    #delete everything in the text field
        self.course_information_text.delete("1.0", tk.END)
    #find the course
        course = self.course_catalog.find_course(course_id)
    #if not found update the course information field with the information
        if course is None:
            self.course_information_text.insert(
                tk.END,
                f"Course {course_id} not found"
            )
        else:
        #call print course to get the course output and update the course informatiojn field
            output = self.course_catalog.print_course(course,True)
            self.course_information_text.insert(tk.END, output)
    """When a row is selected, update the course_information_text field with the course's information"""
    def select_tree_row(self, event):

        selected = self.catalog_tree.focus()
        if not selected:
            return
        #get the values of the item selected
        values = self.catalog_tree.item(selected, "values")

        course_id = values[0]
        #find the course by course_id
        course = self.course_catalog.find_course(course_id)

        self.course_information_text.delete("1.0", tk.END)
        #if the course exists print the information to the course_information_text field
        if course:
            self.course_information_text.insert(
                tk.END,
                self.course_catalog.print_course(course, True)
            )

    """When the add item button is clicked attempts to add an item of the selected type"""
    def add_item(self):
        if self.insert_type_box.get() == "Course":
            self.add_course_form()
        elif self.insert_type_box.get() == "Pre-req":
            self.add_prereq_form()
    """Creates a form to add a course and adds the course if all requirements are met"""
    def add_course_form(self):
        form = tk.Toplevel(self.root)
        form.title("Add Course")
        form.geometry("400x250")

        tk.Label(form, text="Course ID").grid(row=0, column=0, padx=5, pady=5)
        course_id_entry = tk.Entry(form)
        course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Course Name").grid(row=1, column=0, padx=5, pady=5)
        course_name_entry = tk.Entry(form)
        course_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Pre-Requisites(Comma Seperated)").grid(row=2, column=0, padx=5, pady=5)
        prereq_entry = tk.Entry(form)
        prereq_entry.grid(row=2, column=1, padx=5, pady=5)

        error_label = tk.Label(form, text="", fg="red")
        error_label.grid(row=4, column=0, columnspan=2, pady=5)

        def save_course():
            course = Courses.Course()
            course.course_id = course_id_entry.get().strip()
            course.course_name = course_name_entry.get().strip()
            if not course.course_id:
                error_label.config(text = "Course ID can't be blank")
                return
            
            if self.course_catalog.find_course(course.course_id):
                error_label.config(text= "Course ID already exists")
                return
            
            if not course.course_name:
                error_label.config(text = "Course Name can't be blank")
                return
            
            if prereq_entry.get():
                course.prereqs = [p.strip() for p in prereq_entry.get().split(",")]
            for prereq in course.prereqs:
                if self.course_catalog.find_course(prereq) is None:
                        error_label.config(text = f"{prereq} doesn't exist")
                        return
                
            result = self.db.create_course(course.course_id,course.course_name)
            if result:

                for prereq in course.prereqs:
                    self.db.add_prereq(course.course_id, prereq)
                
                self.course_catalog.insert_course(course)
                self.catalog_tree.insert(
                    "",
                    tk.END,
                    iid=course.course_id,
                    values=(course.course_id,course.course_name)
                )
            
            if not result:
                error_label.config(text = "Could not create course")
                return
            
            self.sort_catalog_tree()
            form.destroy()
        tk.Button(form, text="Save", command=save_course).grid(
            row = 3, column = 0, columnspan = 2, pady = 10
        )
    """Creates a prereq form and adds the prereq if both the course and prereq course exists"""
    def add_prereq_form(self):
        form = tk.Toplevel(self.root)
        form.title("Add Course")
        form.geometry("400x250")

        tk.Label(form, text="Higher Course id").grid(row=0, column=0, padx=5, pady=5)
        course_id_entry = tk.Entry(form)
        course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Pre-req course id").grid(row=1, column=0, padx=5, pady=5)
        prereq_entry = tk.Entry(form)
        prereq_entry.grid(row=1, column=1, padx=5, pady=5)

        error_label = tk.Label(form, text="", fg="red")
        error_label.grid(row=3, column=0, columnspan=2, pady=5)

        def save_prereq():
            course_id = course_id_entry.get().strip()
            prereq_id = prereq_entry.get().strip()
            course = self.course_catalog.find_course(course_id)
            if not course_id:
                error_label.config(text = "Higher Course ID can't be blank")
                return
            if not course:
                error_label.config(text = "Higher Course ID doesn't exist")
                return
            if not prereq_id:
                error_label.config(text = "Prereq Course ID can't be blank")
                return
            if self.course_catalog.find_course(prereq_id) is None:
                error_label.config(text = "Prereq Course ID doesn't exist")
                return
            result = self.db.add_prereq(course_id,prereq_id)
            if not result:
                error_label.config(text = "Pre-req already exists")
                return
            self.course_catalog.add_pre_req(course_id,prereq_id)
            self.sort_catalog_tree()
            form.destroy()
        tk.Button(form, text="Save", command=save_prereq).grid(
            row = 2, column = 0, columnspan = 2, pady = 10
        )
    """Refreshes the treeview with the current catalog correctly sorted"""
    def sort_catalog_tree(self):
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)

        self.course_catalog.sort_courses()

        for course in self.course_catalog.course_list:
            self.catalog_tree.insert(
                "",
                tk.END,
                iid=course.course_id,
                values=(course.course_id, course.course_name)
            )
    """Gets the course that is currently displayed in the selecte course frame"""
    def get_displayed_course_id(self):
        text = self.course_information_text.get("1.0",tk.END).strip()

        for line in text.splitlines():
            if line.startswith("Course ID:"):
                return line.replace("Course ID:","", 1).strip()

        return None
    """Removes a row in the catalog tree"""
    def delete_catalog_tree_row(self, course_id):
        if self.catalog_tree.exists(course_id):
            self.catalog_tree.delete(course_id)
            return True
        
        return False
    """Creates a form to delete a course, if the course exists it deletes the course"""
    def delete_course_form(self):
        form = tk.Toplevel(self.root)
        form.title("Delete Course")
        form.geometry("400x250")

        tk.Label(form, text="Course ID").grid(row=0, column=0, padx=5, pady=5)
        course_id_entry = tk.Entry(form)
        course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        error_label = tk.Label(form, text="", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, pady=5)

        def delete_course():
            course_id = course_id_entry.get()
            if not course_id:
                error_label.config(text = "Course ID can't be blank")
                return
            if self.course_catalog.find_course(course_id) is None:
                error_label.config(text = "Course not found")
                return
            if self.db.delete_course(course_id):
                self.course_catalog.remove_prereq_from_courses(course_id)
                self.course_catalog.delete_course(course_id)
                self.course_information_text.delete("1.0", tk.END)
            self.sort_catalog_tree()
            
            form.destroy()
        tk.Button(form, text="Delete", command=delete_course).grid(
            row = 3, column = 0, columnspan = 2, pady = 10
        )

    def delete_prereq_form(self):
        form = tk.Toplevel(self.root)
        form.title("Delete Prereq")
        form.geometry("400x250")

        tk.Label(form, text="Higher Course ID").grid(row=0, column=0, padx=5, pady=5)
        course_id_entry = tk.Entry(form)
        course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Prereq ID").grid(row=0, column=0, padx=5, pady=5)
        prereq_entry = tk.Entry(form)
        prereq_entry.grid(row=1, column=1, padx=5, pady=5)

        error_label = tk.Label(form, text="", fg="red")
        error_label.grid(row=3, column=0, columnspan=2, pady=5)

        def delete_prereq():
            course_id = course_id_entry.get()
            prereq_id = prereq_entry.get()
            if not course_id:
                error_label.config(text = "Higher Course ID can't be blank")
                return
            
            if not prereq_id:
                error_label.config(text = "Prereq Course ID can't be blank")
                return
            course = self.course_catalog.find_course(course_id)

            if course is None:
                error_label.config(text = "Higher Course ID doesn't exist")
                return

            if prereq_id not in course.prereqs:
                error_label.config(text = "Prereq is not in Higher course")
                return

            result = self.db.delete_prereq(course_id,prereq_id)

            if not result:
                error_label.config(text = "Could not delete prereq")
                return
            self.course_catalog.delete_prereq(course_id,prereq_id)

            form.destroy()
        tk.Button(form, text="Delete", command=delete_prereq).grid(
            row = 4, column = 0, columnspan = 2, pady = 10
        )
    def delete_selected_item(self):
        selected_option = self.insert_type_box.get()
        if selected_option == "Course":
            self.delete_course_form()
        elif selected_option == "Pre-req":
            self.delete_prereq_form()

    """Allows a course name to be edited"""
    def edit_course_form(self):
        course_id = self.get_displayed_course_id()

        if not course_id:
            return

        course = self.course_catalog.find_course(course_id)

        if course is None:
            return

        form = tk.Toplevel(self.root)
        form.title("Edit Course")
        form.geometry("400x250")

        tk.Label(
            form,
            text="Course ID"
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(
            form,
            text="Course Name"
        ).grid(row=1, column=0, padx=5, pady=5)

        course_name_entry = tk.Entry(form)
        course_name_entry.grid(row=1,column=1,padx=5,pady=5)
        course_name_entry.insert(0,course.course_name)

        def save_course():
            course_name = course_name_entry.get().strip()


            if not course_name:
                return
            result = self.db.update_course(
                course_id,
                course_name
            )
            if not result:
                return
            
            course.course_name = course_name

            self.catalog_tree.item(
               course_id,
                values=(course_id, course_name)
            )
            form.destroy()

        tk.Button(
            form,
            text="Save",
            command=save_course
        ).grid(row=2,column=0,pady=10)
        