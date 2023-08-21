# Sorting 2

'''
Implement these additional sorting algorithms: Quick, Modified Quick, and Merge.
Test your sorting algorithms as you did in the previous assignment.
'''

import random

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
    # Sort L and R recursively
    mergeSort(L)
    mergeSort(R)
    # Merge L and R over A
    i = 0 # Left index
    j = 0 # Right index
    k = 0 # Merged index
    while i < len(L) and j < len(R): # Merge
        if L[i] <= R[j]:
            A[k] = L[i]
            i+=1
            k+=1
        else:
            A[k] = R[j]
            j+=1
            k+=1
    # Add the leftovers
    while i < len(L):
        A[k] = L[i]
        i+=1
        k+=1
    while j < len(R):
        A[k] = R[j]
        j+=1
        k+=1

def createRandomList(N):
    A = []
    for i in range(N):
        r = random.randrange(N)
        A.append(r)
    return A

def main():
    # Quick sort test
    list1 = createRandomList(15)
    print("List 1: " + str(list1))

    list1Copy = list1[:]
    quickSort(list1, 0, 14)
    list1Copy.sort()

    print("Quick sort: " + str(list1))
    print(list1 == list1Copy)

    # Modified quick sort test
    list2 = createRandomList(15)
    print("List 2: " + str(list2))

    list2Copy = list2[:]
    modifiedQuickSort(list2, 0, 14)
    list2Copy.sort()

    print("Modified quick sort: " + str(list2))
    print(list2 == list2Copy)

    # Merge sort test
    list3 = createRandomList(15)
    print("List 3: " + str(list3))

    list3Copy = list3[:]
    mergeSort(list3)
    list3Copy.sort()

    print("Merge sort: " + str(list3))
    print(list3 == list3Copy)

main()