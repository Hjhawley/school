#include <stdio.h>
#include <stdbool.h>
#include "solve.h"

void print_maze(char field[SIZE_Y][SIZE_X]) {
    for (int y = 0; y < SIZE_Y; y++) {
        for (int x = 0; x < SIZE_X; x++) {
            putchar(field[y][x]); // You can use printf("%c", field[y][x]); as well
        }
        putchar('\n');
    }
}

void solve_maze(char field[SIZE_Y][SIZE_X]) {
    bool madeChange;
    do {
        madeChange = false;

        for (int y = 1; y < SIZE_Y - 1; y++) {
            for (int x = 1; x < SIZE_X - 1; x++) {
                if (field[y][x] == '.') { // Check if the cell is a path
                    int wallCount = 0;

                    // Check surrounding cells for walls
                    if (field[y - 1][x] == '@') wallCount++;
                    if (field[y + 1][x] == '@') wallCount++;
                    if (field[y][x - 1] == '@') wallCount++;
                    if (field[y][x + 1] == '@') wallCount++;

                    // If three walls are found, it's a dead end
                    if (wallCount == 3) {
                        field[y][x] = '@'; // Convert path to wall
                        madeChange = true;
                    }
                }
            }
        }
    } while (madeChange); // Repeat if changes were made
}
