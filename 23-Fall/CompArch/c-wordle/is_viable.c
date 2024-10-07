#include "wordle.h"
#include <string.h>
#include <stdbool.h>

bool is_viable_candidate(char *candidate, guess *guesses, int guess_count) {
    for (int i = 0; i < guess_count; i++) {
        char copy[6];
        strcpy(copy, candidate);

        for (int j = 0; j < 5; j++) {
            if (guesses[i].feedback[j] == EXACT_HIT) {
                if (copy[j] != guesses[i].letters[j]) {
                    return false;
                }
                copy[j] = '_'; // Cross off the letter
            }
        }

        for (int j = 0; j < 5; j++) {
            if (guesses[i].feedback[j] == PARTIAL_HIT && copy[j] == guesses[i].letters[j]) {
                return false;
            }
        }

        for (int j = 0; j < 5; j++) {
            if (guesses[i].feedback[j] == PARTIAL_HIT) {
                bool found = false;
                for (int k = 0; k < 5; k++) {
                    if (copy[k] == guesses[i].letters[j]) {
                        found = true;
                        copy[k] = '_'; // Cross off the letter
                        break;
                    }
                }
                if (!found) {
                    return false;
                }
            }
        }

        for (int j = 0; j < 5; j++) {
            if (guesses[i].feedback[j] == MISS) {
                for (int k = 0; k < 5; k++) {
                    if (copy[k] == guesses[i].letters[j]) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
}
