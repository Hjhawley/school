#include <stdio.h>

void print_line(int spaces, int stars) {
    for (int i = 0; i < spaces; i++) {
        printf(" ");
    }
    for (int i = 0; i < stars; i++) {
        printf("*");
    }
    printf("\n");
}

void print_diamond(int size) {
    int stars, spaces;

    for (int i = 0; i < size; i++) {
        stars = 2 * i + 1;
        spaces = size - i - 1;
        print_line(spaces, stars);
    }

    for (int i = size - 2; i >= 0; i--) {
        stars = 2 * i + 1;
        spaces = size - i - 1;
        print_line(spaces, stars);
    }
}
