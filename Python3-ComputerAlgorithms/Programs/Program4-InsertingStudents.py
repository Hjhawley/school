# Inserting Students
'''
Create a class called Student.
The class should contain all the fields found in FakeNames.txt, which you can get from our Canvas Files page.

Write code to read all the data from FakeNames.txt into a python list of student objects.
Detect any duplicate objects. That is, if a student has the same SSN as a previous student, do not add that student. Instead, print an error message.
Time how long that takes, and have your code print that.
Note of clarification: You should not be changing the input files, or making any output file, and you should have only 1 python list in memory.
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
            print("Error: Duplicate SSN for " + s.mFirstName + " " + s.mLastName)
        else:
            allStudents.append(s)
    f.close()
    end = time.time()
    print("Time: " + str(end - start) + " seconds")

main()