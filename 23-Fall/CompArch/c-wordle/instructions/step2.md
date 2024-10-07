Parsing guesses
---------------

In this step you will write a function `parse_guess` in the file
`parse.c` to parse a single guess with the feedback that the game
gives. In the original game, colors are used to give feedback on a
guess:

*   Green: the letter is correct and in the correct position
*   Yellow: the letter appears in the word, but it was in the wrong
    position
*   Gray: the letter does not appear at all in the word

In `wordle.h` there is a type `guess` defined:

``` c
enum feedback { MISS, EXACT_HIT, PARTIAL_HIT };
typedef struct {
    char letters[6];
    enum feedback feedback[5];
} guess;
```

The `letters` attribute holds the guess itself (with a terminating
null) and `feedback` holds the “color” of each letter as an `enum`:

*   `MISS`: a gray letter (does not appear in solution word)
*   `EXACT_HIT`: a green letter (correct letter in correct position)
*   `PARTIAL_HIT`: a yellow letter (correct letter in incorrect
    position)

You will be given a line of input to parse. Here is an example of a
guess with feedback as it will be given to you:

    [s]t(e)(a)m

All letters will be lower case. If a letter is surrounded by square
brackets (`[s]` in the example) then it is an `EXACT_HIT`. If it is
surrounded by parentheses (`(e)` and `(a)` in the example) then it
is a `PARTIAL_HIT`. An unadorned letter is a `MISS`.

Your job is to parse a line of input and return a `guess` that has
been correctly filled in based on the input. Note that you are
expected to return `guess` by value, not a pointer to a `guess`. You
should ensure that the `letters` attribute has a terminating null
so that it can be treated as either an array of exactly five letters
or as a string of five letters.


### Hints

There are no library functions that will make this significantly
easier—you are probably better off examining the characters of the
input directly.

*   To test if a character is a lower-case letter, you can compare
    it with 'a' and 'z':

        if (ch >= 'a' && ch <= 'z') { ... }

*   You will expect exactly five inputs, but you do not know in
    advance how many characters to expect for each letter. A `for`
    loop will work well for walking over the five positions that you
    need to fill in for the `guess` (both the `letters` and the
    `feedback`), but you should probably track your position in the
    input string separately and advance that cursor as needed:

    *   Start with a pointer to the beginning of the line of input
    *   Check for each of the three possible cases, fill in the
        `letter` and `feedback` entries based on what you find, then
        add one or three to the pointer (depending on how many
        characters you used) so the next iteration of the loop will
        know where to continue parsing.
