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
    start = time.time()
    f = open("FakeNames.txt")
    allStudents = []
    for line in f:
        fields = line.split()
        s = Student(fields[0], fields[1], fields[2], fields[3], fields[4])
        repeat = False
        for i in allStudents:
            if i.mSSN == s.mSSN:
                repeat = True
        if repeat:
            print("Error: Duplicate SSN")
        else:
            allStudents.append(s)
    f.close()
    end = time.time()
    print("Time: " + str(end - start) + " seconds")

main()