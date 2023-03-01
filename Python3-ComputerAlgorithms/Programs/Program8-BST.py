'''
BST
Create another container class for storing unordered unique Students.
It should support the methods: Exists, Insert, Traverse, Delete, Retrieve, and Size.
Implement the methods using a Binary Search Tree (BST).
Repeat the previous assignment using your new BST container class.
Compare the Insert, Traverse, Delete, and Retrieve times to the previous containers.
Verify that the average ages and the error messages are the same.
After you get it working with the regular lists, try it on the Medium sized lists: FakeNamesMedium.txt, DeleteNamesMedium.txt, and RetrieveNamesMedium.txt.
In this case, do not print every student that failed to insert, delete, or retrieve. Just print the total fails in each category.
'''

import time
from student import Student
from bst import BST

ageTotal = 0

def callbackFunction(s):
    global ageTotal
    ageTotal += int(s.mAge)

def main():
    # Insert
    start = time.time()
    f = open("FakeNamesMedium.txt")
    duplicates = 0
    allStudents = BST()
    for line in f:
        fields = line.split()
        s = Student(fields[0], fields[1], fields[2], fields[3], fields[4])
        if allStudents.insert(s) == False:
            duplicates += 1
    print(str(duplicates) + " duplicates for insertion.")
    f.close()
    end = time.time()
    print("Time for insert: " + str(end - start) + " seconds")

    # Traverse
    start = time.time()
    averageAge = 0
    count = allStudents.size()
    allStudents.traverse(callbackFunction)
    averageAge = ageTotal/count
    print("Average age: " + str(averageAge))
    end = time.time()
    print("Time for traverse: " + str(end - start) + " seconds")

    # Delete
    start = time.time()
    f = open("DeleteNamesMedium.txt")
    errors = 0
    for line in f:
        SSN = line.strip()
        s2 = Student("", "", SSN, "", "") # Dummy student
        if allStudents.delete(s2) == False:
            errors += 1
    print(str(errors) + " deletion errors: does not exist.")
    f.close()
    end = time.time()
    print("Time for delete: " + str(end - start) + " seconds")
    
    # Retrieve
    start = time.time()
    f = open("RetrieveNamesMedium.txt")
    errors = 0
    duplicates = 0
    rTotal = 0
    rAge = 0
    for line in f:
        SSN = line.strip()
        s2 = Student("", "", SSN, "", "")
        retrieved = allStudents.retrieve(s2)
        if retrieved is not None:
            rTotal += 1
            rAge += int(retrieved.mAge)
        else:
            errors += 1
    if rTotal == 0:
        print("Error: retrieve count == 0")
    else:
        averageAge = rAge/rTotal
        print("Average age: " + str(averageAge))
    print(str(errors) + " retrieval errors: does not exist.")
    f.close()
    end = time.time()
    print("Time for retrieve: " + str(end - start) + " seconds")

main()