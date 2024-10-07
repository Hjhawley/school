#include "wordle.h"
#include <string.h>
#include <stdio.h>

// a convenient struct to store a potential guess along with its score
struct recommendation {
    int score;
    char word[6];
};

void recommend(char **word_list, guess *guesses, int guess_count) {
    struct recommendation recommendations[RECOMMENDATION_COUNT + 1];
    int recommendations_count = 0;

    for (int i = 0; word_list[i] != NULL; i++) {
        if (is_viable_candidate(word_list[i], guesses, guess_count)) {
            int currentScore = score(word_list, word_list[i], guesses, guess_count);

            recommendations[recommendations_count].score = currentScore;
            strcpy(recommendations[recommendations_count].word, word_list[i]);

            int j = recommendations_count;
            while (j > 0 && (recommendations[j].score > recommendations[j - 1].score ||
                             (recommendations[j].score == recommendations[j - 1].score && strcmp(recommendations[j].word, recommendations[j - 1].word) < 0))) {
                struct recommendation temp = recommendations[j];
                recommendations[j] = recommendations[j - 1];
                recommendations[j - 1] = temp;
                j--;
            }

            if (recommendations_count < RECOMMENDATION_COUNT) {
                recommendations_count++;
            }
        }
    }

    for (int i = 0; i < recommendations_count; i++) {
        printf("%d: %s\n", recommendations[i].score, recommendations[i].word);
    }
}
