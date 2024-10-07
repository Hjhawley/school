#include "compute.h"
#include <string.h>

int compute(char *a, char *b) {
    int distance = 0;

    if (strlen(a) != strlen(b)) {
        return -1; // If string lengths are not equal, return -1
    }

    for (int i = 0; a[i] != '\0'; i++) {
        if (a[i] != b[i]) {
            distance++;
        }
    }

    return distance;
}
