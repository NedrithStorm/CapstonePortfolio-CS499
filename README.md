# CapstonePortfolio-CS499
The project for my CS-499 my professional portfolio and final project

# Professional Self-Assessement

This capstone showed me a number of things.  First, that I can easily translate code that worked in C++ to Python.  Next, That I can work with a library I never used before , Tkinter, and work with it to create a well-functioning GUI.  And furthermore that I can design a database and interact with it using Python without an issue. This was not only my first time using SQLite, but also one of the few times I made in-depth code to interact with a database using Python.

Overall I came up with a number of enhancements to an program we made, designed them, and then implemented over a short period of time.  The enhancement started with a week to plan it, a week to review the code, and then one week for each of the 3 enhancements.  I did all of this in my free time while going to work and living a relatively normal life.  I think this project showcases not only my software engineering and database skills but also my ability to be adaptable and learn new things.  It also showcases my ability to understand DSA concepts such as big-O notation and writing code to determine performance improvements when needed.  I was able to create a secure project, communicate weekly with my instructor on how progress was going, and create a professional code review that when done with others will allow us to ensure that we are writing code that is as high quality as possible by finding areas of improvements and parts that went well.

Overall I hope that anyone looking at this project will like how a took a simple console based course planner and turned it into one where courses can be added, saved, and with a GUI that makes it look a bit more modern and is easier to use than a console application all done in a short period of time.

# Code Review

During the course we were asked to do a code review of the artifact(s) we chose to enhance.  Since I'm using the same artifact for all of the enhancements I had to do a 30 minute code review of my course planning software from CS-300 Data Structures and Algorithms.  Overall the code was well written but I found a few issues with my comments for the Courses class and missing input validation which introduced a critical flaw

[![Code Review Video Thumbnail](https://img.youtube.com/vi/Xk2EULd66Gw/hqdefault.jpg)](https://youtu.be/Xk2EULd66Gw)

*Click the image above to watch the video on YouTube.*

# Original Artifact

In CS-300 Data Structures and Algorithms we were asked to design algorithms for arrays, binary search trees, and hash tables for a course planning software.  The software had to read a .csv file, validate that a course existed for every pre-requisite, print out a list of all courses, and also find a print a specific course with any pre-requisites.  After designing the algorithms we were then asked to determine which data structure made sense for the software and then code the software.  It was a quick and simple program that was to be written in C++ as a console application. For the software I ended up using an array.

<img width="856" height="498" alt="image" src="https://github.com/user-attachments/assets/f5946d21-c803-4071-ba47-9d0a0fc41da5" />


# Enhancement 1 : Software enginerring

For my first enhancement I wanted to transfer the code to Python and then use Tkinter to build a GUI for the software.  Console applications are simple to make and fine for a small program but for a real course planner that might be the start to something like a Learning Management System(LMS) that a college might use, a GUI is a lot more easier to use and more professional.

<img width="784" height="434" alt="image" src="https://github.com/user-attachments/assets/e95d6c43-a7d4-4a93-9d45-10bbc96eebb5" />

Using this GUI the planner would load up "courses.csv" read it and give a list of all courses in alphabetical order.  The user can then click on a course or type in the course ID that they want to find and it will display the ID, Name, and any prerequisites

# Enhancement 2: Data Structures and Algorithms

For enhancement 2 I decided to add a hash table into the mix and look at the difference it made.  There are plenty of benefits to using an array.  Arrays are easier to manage and it's far easier to print an array and go in alphabetical order.  These features can be important for our needs.  However, a hash table is far quicker to search and doesn't need to be sorted to take advantage of search algorithms like binary search.  So I created the code to use a hash table, wrote automated testing to test various parts of the code, and also created a small Perormance_test.py file to showcase the difference between searching a hash table and an array.

<img width="483" height="305" alt="image" src="https://github.com/user-attachments/assets/5116bbe0-9830-47f7-93ff-f98911a44a75" />

Overall this enhancement was an optimization and QOL enhancement.  The automated testing will make it easier to find issues before they become a problem.

# Enhancement 3: Databases

A .csv file is a weakness to the software.  It would be hard to share a .csv file with multiple users or in an online setting.  For enhancement 3 I decided to instead move to a SQLite database.  Eventually this would move to SQL using something like MySQL for a full stack software solution.  For this enhancement I wanted the user to be able to add courses and pre-requisites.  I wanted courses to be able to be deleted and updated as well.  I designed the database to currently have 2 tables.  The course table which is a table with the Course ID and the Course Name.  Also a pre-requisite table that has an auto-incrementing primary key along with each row having a course ID and the prerequisite course ID.  This allows any course to have any number of prerequisite as each prerequisite course would be a new row in the table.

<img width="631" height="438" alt="image" src="https://github.com/user-attachments/assets/46a5d1e7-ee56-4bfa-adc8-aa85677864af" />

<img width="367" height="255" alt="image" src="https://github.com/user-attachments/assets/50276aeb-319d-4ebb-a066-d55de274cfc2" />

I also did a lot of code cleanup and designing of additional tests.  The GUI was move into its own class, added a database class, and overall made future changes a lot easier.

