Scoring a candidate word
------------------------

In this step you will take a potential next guess, compare it
against all words in the word list, and come up with a score for how
good a guess it is. We will use a very simple scoring mechanism:

*   If a word in the list is not viable according to the
    `is_viable_candidate` function, ignore it and move on to the
    next word.

*   For a viable word in the list, assume it is the solution to the
    puzzle and give the guess a simple score based on that
    assumption:

    *   Give 5 points for every letter that would appear green
    *   Give 1 point for every letter that would appear yellow
    *   Give 0 points for every letter that would appear gray

*   Repeat this test for every word in the word list and return the
    sum of all the scores.

The scoring method is pretty unsophisticated and arbitrary,
especially in the choice of 5 and 1 points. These constant values
are defined in `wordle.h` and you should use `EXACT_HIT_POINTS` and
`PARTIAL_HIT_POINTS` instead of 5 and 1, respectively.

In the file `score.c` write the function `score` to match the
prototype given in `wordle.h`.

You are given the entire word list (since you need to find and score
every viable word), the candidate guess, and the list of prior
guesses with its count.

Loop over the words in the word list and test each one using
`is_viable_candidate`. If the word is not viable, skip it and move
on. For a viable word:

*   Make a local copy so you cross letters off

*   Loop over the 5 positions of the candidate and look for exact
    hits (under the assumption that the copied word from the list is
    the solution). If the candidate and the copy have a match in the
    same position, cross it off the copy and add 5 to the score.

*   Loop over the 5 positions again looking for partial hits. For
    each letter in the candidate, scan all 5 letters in the copy. If
    you find a match, cross it off the copy and add 1 to the score.
    Be sure to break out of the loop as well so you do not count a
    letter twice.

Return the sum of all the scores that you find for viable words.
