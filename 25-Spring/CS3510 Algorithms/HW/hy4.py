import numpy as np
import time

def naiveMultiply(A, B):
    # Get the dimension of the square matrices
    n = A.shape[0]
    # Initialize the result matrix C with zeroes
    C = np.zeros((n, n), dtype=A.dtype)
    # compute each element of C
    for i in range(n):
        for j in range(n):
            # Dot product of row i and column j
            s = 0
            for k in range(n):
                s += A[i, k] * B[k, j]
            C[i, j] = s
    return C

def add(A, B):
    return A + B

def subtract(A, B):
    return A - B

def strassenMultiply(A, B, threshold=128):
    n = A.shape[0]
    # If the matrix size is below or equal to the threshold, switch to naive multiplication to avoid deep recursion
    if n <= threshold:
        return naiveMultiply(A, B)

    # Split n x n into four quadrants
    mid = n // 2

    # Partition the matrix A into quadrants A11, A12, A21, A22
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    # Partition the matrix B into quadrants B11, B12, B21, B22
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    # Strassen's 7 product formulas, computed recursively
    M1 = strassenMultiply(add(A11, A22), add(B11, B22), threshold)
    M2 = strassenMultiply(add(A21, A22), B11, threshold)
    M3 = strassenMultiply(A11, subtract(B12, B22), threshold)
    M4 = strassenMultiply(A22, subtract(B21, B11), threshold)
    M5 = strassenMultiply(add(A11, A12), B22, threshold)
    M6 = strassenMultiply(subtract(A21, A11), add(B11, B12), threshold)
    M7 = strassenMultiply(subtract(A12, A22), add(B21, B22), threshold)

    # Combine the 7 products to form the four quadrants of the result
    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    # Stack the quadrants horizontally (top row) and vertically (bottom row)
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    
    # Final assembled matrix
    return np.vstack((top, bottom))

def matrices_equal(C1, C2):
    return np.allclose(C1, C2, atol=1e-6)

def test_multiplication():
    print(f"{'Size':<8}{'Naive Time':<16}{'Strassen Time':<24}{'Correct?'}")
    print('-' * 60)
    for n in [64, 128, 256, 512]:
        A = np.random.randint(0, 10, size=(n, n))
        B = np.random.randint(0, 10, size=(n, n))
        
        start = time.perf_counter()
        C_naive = naiveMultiply(A, B)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        C_strassen = strassenMultiply(A, B)
        strassen_time = time.perf_counter() - start

        correct = matrices_equal(C_naive, C_strassen)

        print(f"{n:<8}{naive_time:<18.5f}{strassen_time:<20.5f}{'Yes' if correct else 'No'}")

if __name__ == "__main__":
    test_multiplication()
