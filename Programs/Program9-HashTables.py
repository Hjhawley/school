'''
Hash Table
Repeat the previous assignment using a Hash Table implementation
Compare your results to the BST results for the normal and medium sized lists.
'''

# FakeNames = 30,000
# FakeNamesMedium = 300,000

import time
from student import Student
from hashtable import Hash

ageTotal = 0

def callbackFunction(s):
    global ageTotal
    ageTotal += int(s.mAge)

def main():
    # Insert
    start = time.time()
    f = open("FakeNamesMedium.txt")
    duplicates = 0
    allStudents = Hash(300000)
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

main()

'''
From Program 8:

47 duplicates for insertion.
Time for insert: 47.60763072967529 seconds
Average age: 42.819855110634
Time for traverse: 2.409877300262451 seconds
8 deletion errors: does not exist.
Time for delete: 19.16256856918335 seconds
Average age: 49.5199871083403
12 retrieval errors: does not exist.
Time for retrieve: 9.269023180007935 seconds
'''