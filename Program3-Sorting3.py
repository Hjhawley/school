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
import math
import sys
sys.setrecursionlimit(1800) # For Quick Sort on mostly sorted data

class Counter:
    def __init__(self):
        self.compares = 0

def bubbleSort(A, low, high, c):
    swap = True
    while swap:
        swap = False
        for i in range(len(A)-1):
            c.compares += 1
            if A[i] > A[i+1]:
                A[i],A[i+1] = A[i+1],A[i]
                swap = True

def shakerSort(A, low, high, c):
    swap = True
    while swap:
        swap = False
        for i in range(len(A)-1):
            c.compares += 1
            if A[i] > A[i+1]:
                A[i],A[i+1] = A[i+1],A[i]
                swap = True
        for i in range(len(A)-1, 0, -1):
            c.compares += 1
            if A[i] < A[i-1]:
                A[i],A[i-1] = A[i-1],A[i]
                swap = True

def countingSort(A, low, high, c):
    tally = [0] * len(A)
    for i in A:
        c.compares += 1
        tally[i] += 1
    k = 0
    for i in range(len(tally)):
        value = i
        count = tally[i]
        for j in range(count):
            A[k] = value
            k += 1

def mergeSort(A, low, high, c):
    if len(A) <= 1:
        return
    mid = len(A)//2
    L = A[:mid]
    R = A[mid:]
    mergeSort(L, low, high, c)
    mergeSort(R, low, high, c)
    li = 0
    ri = 0
    mi = 0
    while li < len(L) and ri < len(R):
        c.compares += 1
        if L[li] <= R[ri]:
            A[mi] = L[li]
            li+=1
            mi+=1
        else:
            A[mi] = R[ri]
            ri+=1
            mi+=1
    while li < len(L):
        c.compares += 1
        A[mi] = L[li]
        li+=1
        mi+=1
    while ri < len(R):
        c.compares += 1
        A[mi] = R[ri]
        ri+=1
        mi+=1

def quickSort(A, low, high, c):
    if high - low <= 0:
        return
    lmgt = low + 1
    for i in range(low + 1, high + 1):
        if A[i] < A[low]:
            c.compares += 1
            A[i], A[lmgt] = A [lmgt], A[i]
            lmgt += 1
    pivot = lmgt - 1
    A[low], A[pivot] = A[pivot], A[low]
    quickSort(A, low, pivot-1, c)
    quickSort(A, pivot+1, high, c)

def modifiedQuickSort(A, low, high, c):
    if high - low <= 0:
        return
    mid = (low + high)//2
    A[low],A[mid] = A[mid],A[low] # Modified
    lmgt = low + 1
    for i in range(low + 1, high + 1):
        if A[i]<A[low]:
            c.compares += 1
            A[i],A[lmgt] = A [lmgt],A[i]
            lmgt += 1
    pivot = lmgt - 1
    A[low],A[pivot] = A[pivot],A[low]
    modifiedQuickSort(A, low, pivot-1, c)
    modifiedQuickSort(A, pivot+1, high, c)

def logFormat(x):
    if x!=0:
        x = math.log(x)/math.log(2)
    return x

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

def main(dataSet, title):
    sorts = [bubbleSort, shakerSort, countingSort, mergeSort, quickSort, modifiedQuickSort]
    dataSize = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    topRow = ["Bubble","Shaker","Counting","Merge","Quick","MQuick"]
    print(title)
    print("  ", end="")
    for i in topRow:
        print("%11s" % (i), end="")
    print("")
    for n in dataSize:
        print("%02d" % (int(logFormat(n))), end="")
        for sort in sorts:
            A = dataSet(n)
            B = A[:]
            c = Counter()
            sort(A, 0, len(A)-1, c)
            B.sort()
            x = logFormat(c.compares)
            print("      %05.2f" % (x), end="")
            if A != B:
                print("Error - not sorted properly")
        print("")

main(createRandomList, "Counting compares on random data")
main(createMostlySortedList, "Counting compares on mostly sorted data")