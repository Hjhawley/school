#include "wordle.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char **read_word_list(char *filename) {
    int capacity = 32;
    int length = 0;
    char **words = malloc(capacity * sizeof(char *));
    if (words == NULL) {
        return NULL; // Memory allocation failed
    }

    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        free(words);
        return NULL; // File open failed
    }

    char line[16];
    while (fgets(line, 16, fp)) {
        if (strlen(line) != 6 || line[5] != '\n') { // 5 letters + newline
            // Handle error for invalid line format
            fclose(fp);
            free(words);
            return NULL;
        }

        if (length == capacity) {
            capacity *= 2;
            char **temp = realloc(words, capacity * sizeof(char *));
            if (temp == NULL) {
                // Handle reallocation error
                fclose(fp);
                free(words);
                return NULL;
            }
            words = temp;
        }

        line[5] = '\0'; // Remove newline
        words[length] = malloc(6 * sizeof(char)); // 5 letters + '\0'
        if (words[length] == NULL) {
            // Handle memory allocation error for the word
            fclose(fp);
            free(words);
            return NULL;
        }
        strcpy(words[length], line);
        length++;
    }

    // Add NULL pointer to mark the end of the array
    if (length == capacity) {
        char **temp = realloc(words, (capacity + 1) * sizeof(char *));
        if (temp == NULL) {
            // Handle reallocation error
            fclose(fp);
            free(words);
            return NULL;
        }
        words = temp;
    }
    words[length] = NULL;

    fclose(fp);
    return words;
}

void free_word_list(char **list) {
    if (list == NULL) {
        return;
    }

    for (int i = 0; list[i] != NULL; i++) {
        free(list[i]);
    }
    free(list);
}
