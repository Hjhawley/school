# Sorting 1

'''Implement the bubble sort, shaker sort, and counting sort as Python functions.
You will also need a function to create a random list of N integers, duplicates allowed.
Put it all together inside a main function.
Also, test to make sure all your sorting functions are working.
Do this by copying the original list, useing the built in Python sort method on the copy, then checking if your sorted list matches the sorted copy.
Do this multiple times to verify that each of your sorting algorithms are working.'''

import random

def bubbleSort(A):
    swap = True
    while swap:
        swap = False
        for i in range(len(A)-1):
            if A[i] > A[i+1]:
                A[i],A[i+1] = A[i+1],A[i] # Swap
                swap = True

def shakerSort(A):
    swap = True
    while swap:
        swap = False
        for i in range(len(A)-1):
            if A[i] > A[i+1]:
                A[i],A[i+1] = A[i+1],A[i] # Swap
                swap = True
        for i in range(len(A)-1, 0, -1):
            if A[i] < A[i-1]:
                A[i],A[i-1] = A[i-1],A[i] # Swap
                swap = True

def countingSort(A):
    tally = [0] * len(A)
    for i in A:
        tally[i] += 1
    k = 0
    for i in range(len(tally)):
        value = i
        count = tally[i]
        for j in range(count):
            A[k] = value
            k += 1

def createRandomList(N):
    A = []
    for i in range(N):
        r = random.randrange(N)
        A.append(r)
    return A

def main():
    # Bubble sort test
    list1 = createRandomList(15)
    print(list1)

    list1Copy = list1[:]
    bubbleSort(list1)
    list1Copy.sort()

    print(list1)
    print(list1 == list1Copy)

    # Shaker sort test
    list2 = createRandomList(15)
    print(list2)

    list2Copy = list2[:]
    shakerSort(list2)
    list2Copy.sort()

    print(list2)
    print(list2 == list2Copy)

    # Counting sort test
    list3 = createRandomList(15)
    print(list3)

    list3Copy = list3[:]
    countingSort(list3)
    list3Copy.sort()

    print(list3)
    print(list3 == list3Copy)

main()