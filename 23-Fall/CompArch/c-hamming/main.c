#include <stdio.h>
#include "compute.h"

struct test_case {
    char *a;
    char *b;
    int distance;
};

#define TEST_COUNT 9

struct test_case tests[TEST_COUNT] = {
    { "", "", 0 },
    { "A", "A", 0 },
    { "G", "T", 1 },
    { "GGACTGAAATCTG", "GGACTGAAATCTG", 0 },
    { "GGACGGATTCTG", "AGGACGGATTCT", 9 },
    { "AATG", "AAA", -1 },
    { "ATA", "AGTG", -1 },
    { "", "G", -1 },
    { "G", "", -1 },
};

int main(void) {
    char *blank = "";
    for (int i = 0; i < TEST_COUNT; i++) {
        printf("%sTesting strings \"%s\" and \"%s\"\n", blank,
            tests[i].a, tests[i].b);
        int result = compute(tests[i].a, tests[i].b);
        printf("Expected result was %d, actual result was %d\n",
            tests[i].distance, result);
        blank = "\n";
    }

    return 0;
}
