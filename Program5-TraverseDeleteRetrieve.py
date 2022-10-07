# Traverse, Delete, Retrieve
'''
Enhance the last assignment.
Traverse all students in the pythonList, and print their average age (as a Float, not an Int). Print how many seconds that took.
Delete all students in DeleteNames.txt, and print how long that took.
Retrieve all students in RetrieveNames.txt, print their average age (again, with decimal accuracy), and how long that took.
Also, be sure to print any SSN numbers from the Retrieve and Delete lists that were not there.
'''

import time
from student import Student

def main():
    # Insert
    start = time.time()
    f = open("FakeNames.txt") # Replace 
    allStudents = []
    for line in f:
        fields = line.split()
        s = Student(fields[0], fields[1], fields[2], fields[3], fields[4])
        repeat = False
        for i in allStudents:
            if i.mSSN == s.mSSN:
                repeat = True
        if repeat:
            print("Error: Duplicate SSN for " + s.mFirstName + " " + s.mLastName)
        else:
            allStudents.append(s)
    f.close()
    end = time.time()
    print("Time for insert: " + str(end - start) + " seconds")
    
    # Traverse
    start = time.time()
    count = 0
    totalAge = 0
    for s in allStudents:
        count += 1
        totalAge += int(s.mAge)
    averageAge = totalAge/count
    print("Average age: " + str(averageAge))
    end = time.time()
    print("Time for traverse: " + str(end - start) + " seconds")

    # Delete
    start = time.time()
    f = open("DeleteNames.txt")
    for line in f:
        for i in allStudents:
            if i.mSSN == line:
                allStudents.pop(i)
    f.close()
    end = time.time()
    print("Time for delete: " + str(end - start) + " seconds")
    
    # Retrieve
    start = time.time()
    f = open("RetrieveNames.txt")
    f.close()
    end = time.time()
    print("Time for retrieve: " + str(end - start) + " seconds")

main()