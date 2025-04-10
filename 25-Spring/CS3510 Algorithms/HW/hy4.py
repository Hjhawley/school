import numpy as np
import time

def naiveMultiply(A, B):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=A.dtype)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C

def add(A, B):
    return A + B

def subtract(A, B):
    return A - B

def strassenMultiply(A, B, threshold=64):
    n = A.shape[0]
    if n <= threshold:
        return naiveMultiply(A, B)

    mid = n // 2

    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    M1 = strassenMultiply(add(A11, A22), add(B11, B22), threshold)
    M2 = strassenMultiply(add(A21, A22), B11, threshold)
    M3 = strassenMultiply(A11, subtract(B12, B22), threshold)
    M4 = strassenMultiply(A22, subtract(B21, B11), threshold)
    M5 = strassenMultiply(add(A11, A12), B22, threshold)
    M6 = strassenMultiply(subtract(A21, A11), add(B11, B12), threshold)
    M7 = strassenMultiply(subtract(A12, A22), add(B21, B22), threshold)

    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    # Combine submatrices
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))

# Helper to check if two matrices are "close enough"
def matrices_equal(C1, C2):
    return np.allclose(C1, C2, atol=1e-6)

# Main test function
def test_multiplication():
    print(f"{'Size':<8}{'Naive Time (s)':<18}{'Strassen Time (s)':<20}{'Correct?'}")
    print('-' * 60)
    for n in [64, 128, 256, 512]:
        A = np.random.randint(0, 10, size=(n, n))
        B = np.random.randint(0, 10, size=(n, n))

        start = time.time()
        C_naive = naiveMultiply(A, B)
        naive_time = time.time() - start

        start = time.time()
        C_strassen = strassenMultiply(A, B)
        strassen_time = time.time() - start

        correct = matrices_equal(C_naive, C_strassen)

        print(f"{n:<8}{naive_time:<18.5f}{strassen_time:<20.5f}{'Yes' if correct else 'No'}")

# Run it
if __name__ == "__main__":
    test_multiplication()
