import time
import random
from Courses import Course, Courses

"""
Creates a catalog with number_of_courses courses and does searches searches
Does the searches using an array of courses and a hash table of courses
Prints the time it took to do the searches with a binary search of the array
and a hash table lookup of the hash table

"""
def performance_test(number_of_courses,searches):


    #always use the same seed for repeatable tests
    random.seed(58)

    #create the catalog and get search targets
    catalog = add_courses(number_of_courses)

    search_targets = [
        random.choice(catalog.course_list).course_id
        for _ in range(searches)
    ]

    #start time forq the performance counter
    start = time.perf_counter()

    #run the binary searches
    for target in search_targets:
        catalog.find_course(target,False)
    
    #time difference
    binary_time = time.perf_counter() - start

    #repeat for the hash search
    start = time.perf_counter()

    for target in search_targets:
        catalog.find_course(target,True)

    hash_time = time.perf_counter() - start

    #print out the results of the test
    print(f"Performance test with {number_of_courses} courses and {searches} searches!\n")
    print(f"Binary search completed in {binary_time:.6f} seconds")
    print(f"Hash table lookup completed in {hash_time:.6f} seconds")
    print(f"Hash table is {binary_time/hash_time:.2f}x faster\n\n")

""" Returns a catalog of number_of_courses courses"""
def add_courses(number_of_courses):
    courses = Courses()
    for i in range(number_of_courses):
        course = Course()


        #generate unique course
        course.course_id = f"CSCI{i}"
        course.course_name = f"Course Name {i}"
        course.prereqs = []

        courses.insert_course(course)

    return courses

def main():
    #run 4 performance tests
    performance_test(1000,10000)
    performance_test(10000,100000)
    performance_test(100000,1000000)
    performance_test(1000000,10000000)

if __name__ == "__main__":
    main()