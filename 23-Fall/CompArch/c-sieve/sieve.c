#include <stdbool.h>

void sieve(bool *arr, int size) {
    arr[0] = false; // 0 is not prime
    arr[1] = false; // 1 is not prime
    for (int i = 2; i < size; i++) {
        arr[i] = true;
    }

    for (int i = 2; i * i < size; i++) {
        if (!arr[i]) {
            continue; // Skip if number is already marked 'false'
        }

        // Cross off multiples i
        for (int j = i * i; j < size; j += i) {
            arr[j] = false;
        }
    }
}
