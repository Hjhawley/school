#include "wordle.h"
#include <string.h>

int score(char **word_list, char *candidate, guess *guesses, int guess_count) {
    int totalScore = 0;

    for (int i = 0; word_list[i] != NULL; i++) {
        if (is_viable_candidate(word_list[i], guesses, guess_count)) {
            char copy[6];
            strcpy(copy, word_list[i]);
            int wordScore = 0;

            // Check for exact hits
            for (int j = 0; j < 5; j++) {
                if (candidate[j] == copy[j]) {
                    wordScore += EXACT_HIT_POINTS;
                    copy[j] = '_'; // Cross off the letter
                }
            }

            // Check for partial hits
            for (int j = 0; j < 5; j++) {
                for (int k = 0; k < 5; k++) {
                    if (candidate[j] == copy[k]) {
                        wordScore += PARTIAL_HIT_POINTS;
                        copy[k] = '_'; // Cross off the letter
                        break;
                    }
                }
            }

            totalScore += wordScore;
        }
    }

    return totalScore;
}
