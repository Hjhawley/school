# Sorting 3
'''
Measure all 6 sorting algorithms by counting the number of compares.
Test on data ranging from size 8 to size 2k, by powers of 2.
Test on random data and on mostly sorted data.
(Make a new function to create mostly sorted data. Have it first call the MakeRandomData function, have Python sort it, then swap the first and last elements.)

Print all this data in organized tables, that you can then copy into Excel spreadsheets for making charts.
You will need to create two data sets, with 1 Excel chart for each.
The first data set and chart should plot Problem Size versus number of Compares when using Random data.
The second data set and chart should plot Problem Size versus number of Compares when using Mostly Sorted data instead of Random data.
To pass off, show the data sets and charts that illustrate compares for random and mostly sorted data. Be prepared to explain what they mean.

It is important to make the charts Log/Log. That is, modify your python code to print the Log of the Problem Size and the Log of the number of Comparisons.
Otherwise it will be really hard to see and interpret the results.
Also, make an effort to organize your python code to reduce repeating code as much as possible.
'''

import random

class Counter:
    def __init__(self):
        self.compares = 0

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

def quickSort(A, low, high):
    if high - low <= 0:
        return
    lmgt = low + 1
    for i in range(low + 1, high + 1):
        if A[i] < A[low]:
            A[i], A[lmgt] = A [lmgt], A[i]
            lmgt += 1
    pivot = lmgt - 1
    A[low], A[pivot] = A[pivot], A[low]
    quickSort(A, low, pivot-1)
    quickSort(A, pivot+1, high)

def modifiedQuickSort(A, low, high):
    if high - low <= 0:
        return
    mid = (low + high)//2
    A[low],A[mid] = A[mid],A[low] # Modified
    lmgt = low + 1
    for i in range(low + 1, high + 1):
        if A[i]<A[low]:
            A[i],A[lmgt] = A [lmgt],A[i]
            lmgt += 1
    pivot = lmgt - 1
    A[low],A[pivot] = A[pivot],A[low]
    modifiedQuickSort(A, low, pivot-1)
    modifiedQuickSort(A, pivot+1, high)

def mergeSort(A):
    if len(A) <= 1:
        return
    mid = len(A)//2
    L = A[:mid]
    R = A[mid:]
    mergeSort(L)
    mergeSort(R)
    li = 0 # Left index
    ri = 0 # Right index
    mi = 0 # Merged index
    while li < len(L) and ri < len(R): # Merge
        if L[li] <= R[ri]:
            A[mi] = L[li]
            li+=1
            mi+=1
        else:
            A[mi] = R[ri]
            ri+=1
            mi+=1
    while li < len(L):
        A[mi] = L[li]
        li+=1
        mi+=1
    while ri < len(R):
        A[mi] = R[ri]
        ri+=1
        mi+=1

def createRandomList(N):
    A = []
    for i in range(N):
        r = random.randrange(N)
        A.append(r)
    return A

def createMostlySortedList(N):
    A = createRandomList(N)
    A.sort()
    A[0],A[-1] = A[-1],A[0]
    return A

def main():
    sorts = [bubbleSort, shakerSort, countingSort, quickSort, modifiedQuickSort, mergeSort]
    for sort in sorts:
        A = createRandomList(10)
        B = A[:]
        #c = counter()
        print(str(A) + " - Unsorted")
        sort(A)
        print(str(A) +" - "+ str(sort))
        B.sort()
        if A != B:
            print("Error")

'''
my_l = createRandomList(15)
print(my_l)
my_l = createMostlySortedList(15)
print(my_l)
'''

main()