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
from uuc import UUC

# studentList = UUC()
# for line in f

def traverse():
    start = time.time()
    f = open("FakeNames.txt")
    count = 0
    totalAge = 0
    allStudents = []
    for line in f:
        fields = line.split()
        s = Student(fields[0], fields[1], fields[2], fields[3], fields[4])
        repeat = False
        for i in allStudents:
            if i.mSSN == s.mSSN:
                repeat = True
            else:
                count += 1
                totalAge += int(i.mAge)
        if repeat:
            print("Error: Duplicate SSN for " + s.mFirstName + " " + s.mLastName)
        else:
            allStudents.append(s)
    averageAge = totalAge/count
    f.close()
    end = time.time()
    print("Average age: " + str(averageAge))
    print("Time: " + str(end - start) + " seconds")

def delete():
    pass

def retrieve():
    pass

def main():
    traverse()

main()