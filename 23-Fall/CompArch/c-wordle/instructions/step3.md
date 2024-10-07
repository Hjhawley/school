Testing if a word is a viable guess
-----------------------------------

Given a list of prior guesses and feedback on them, in this step you
will test if a word is a potential solution that incorporates all
feedback. For example, given this sequence of guesses and feedback:

    a(r)i(s)(e)
    [r]o(u)t(e)

You would reject `super` (it has valid letters but does not have an
'r' in the first position) and you would accept `rules` (it has an
'r' as the first letter, a 'u' that is not the third letter, an
'e' that is not the last letter, an 's' that is not the fourth
letter, and it does not contain 'a', 'i', 'o', or 't').

In the file `is_viable.c` write a function `is_viable_candidate`
that matches the prototype in `wordle.h`.

You are given a candidate word to test and the list of guesses (with
a count so you know how many there are). I suggest the following
approach:

*   Loop over the guesses and try to eliminate the candidate and if
    you can find a reason to rule it out return false
*   If none of the information learned from prior guesses makes this
    candidate invalid, then return true

For each guess that you are considering, start by making a copy of
the candidate into a local variable (you can use `strcpy`):

``` c
char copy[6];
strcpy(copy, candidate);
```

This will allow you to cross letters off the word (see below)
without losing the original word.

Now perform a series of tests in order:

1.  Loop over the five letters of the guess and check for
    `EXACT_HIT` letters. If you find one and the corresponding
    position in the candidate is a mismatch, return false. If it is
    a match, cross it off the candidate (put a non-letter character
    like a '_' in that position).

2.  Loop over the five letters of the guess again and check for
    `PARTIAL_HIT` letters. When you find one, check if the candidate
    has a matching letter in the same position. If so, return false.

3.  Loop over the five letters again and check for `PARTIAL_HIT`
    letters again. This time, when you find one scan all five
    positions of the candidate to look for a match. If you find one,
    cross it off (as before) and break out of the loop (you do not
    want to inadvertently cross it off twice in two different
    positions). If you do not find the letter anywhere, then return
    false.

4.  Loop over the five letters again, this time looking for `MISS`
    letters. When you find one in the guess, scan all the positions
    in the candidate and make sure there are no matches. If you find
    a match, return false.

This sequencing will correctly handle words with the same letter
appearing twice. Try following the procedure by hand on a few
examples to make sure you understand how it works.
