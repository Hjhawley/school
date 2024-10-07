#include "wordle.h"
#include <stdio.h>

guess parse_guess(char *line) {
    guess g;
    int line_index = 0, guess_index = 0;

    while (guess_index < 5 && line[line_index] != '\0') {
        if (line[line_index] == '[') {
            // Exact hit
            g.letters[guess_index] = line[line_index + 1];
            g.feedback[guess_index] = EXACT_HIT;
            line_index += 3; // Skip over the green letter
        } else if (line[line_index] == '(') {
            // Partial hit
            g.letters[guess_index] = line[line_index + 1];
            g.feedback[guess_index] = PARTIAL_HIT;
            line_index += 3; // Skip over the yellow letter
        } else if (line[line_index] >= 'a' && line[line_index] <= 'z') {
            // Miss
            g.letters[guess_index] = line[line_index];
            g.feedback[guess_index] = MISS;
            line_index += 1; // Move to next character
        } else {
            line_index += 1;
        }

        guess_index++;
    }

    g.letters[5] = '\0';
    return g;
}
