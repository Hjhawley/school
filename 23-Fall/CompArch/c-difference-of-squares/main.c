#include <stdio.h>
#include "difference_of_squares.h"

struct test_case {
    unsigned int number;
    unsigned int difference;
};

#define TEST_COUNT_SQUARE_OF_SUM 3
#define TEST_COUNT_SUM_OF_SQUARES 3
#define TEST_COUNT_DIFFERENCE 3

struct test_case tests_square_of_sum[TEST_COUNT_SQUARE_OF_SUM] = {
    { 1, 1 },
    { 5, 225 },
    { 100, 25502500 },
};

struct test_case tests_sum_of_squares[TEST_COUNT_SUM_OF_SQUARES] = {
    { 1, 1 },
    { 5, 55 },
    { 100, 338350 },
};

struct test_case tests_difference[TEST_COUNT_DIFFERENCE] = {
    { 1, 0 },
    { 5, 170 },
    { 100, 25164150 },
};

int main(void) {
    char *blank = "";
    for (int i = 0; i < TEST_COUNT_SQUARE_OF_SUM; i++) {
        printf("%sTesting square_of_sum with input %u\n", blank,
            tests_square_of_sum[i].number);
        unsigned int result = square_of_sum(tests_square_of_sum[i].number);
        printf("Expected result was %u, actual result was %u\n",
            tests_square_of_sum[i].difference, result);
        blank = "\n";
    }

    for (int i = 0; i < TEST_COUNT_SUM_OF_SQUARES; i++) {
        printf("%sTesting sum_of_squares with input %u\n", blank,
            tests_sum_of_squares[i].number);
        unsigned int result = sum_of_squares(tests_sum_of_squares[i].number);
        printf("Expected result was %u, actual result was %u\n",
            tests_sum_of_squares[i].difference, result);
        blank = "\n";
    }

    for (int i = 0; i < TEST_COUNT_DIFFERENCE; i++) {
        printf("%sTesting difference_of_squares with input %u\n", blank,
            tests_difference[i].number);
        unsigned int result = difference_of_squares(tests_difference[i].number);
        printf("Expected result was %u, actual result was %u\n",
            tests_difference[i].difference, result);
        blank = "\n";
    }

    return 0;
}
