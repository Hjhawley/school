Word list
---------

This problem has five steps. In the first step you will read a list
of 5-letter words from the file `words.txt`, where each word appears
on a line by itself, into an array of strings. The end result should
be an array of strings, which looks something like this:

```
       +--------+
    0: | char * | --> "aahed"
       +--------+
    1: | char * | --> "aalii"
       +--------+
    2: | char * | --> "aargh"
       +--------+
    3: | char * | --> "aarti"
       +--------+
    4: | char * | --> "abaca"
       +--------+
    5: | char * | --> "abaci"
       +--------+
       |...     |
       +--------+
12970: | char * | --> "zymes"
       +--------+
12971: | char * | --> "zymic"
       +--------+
       | NULL   |
       +--------+
```

The type of this array is `char **`, meaning it is an array of
string pointers.


### `read_word_list`

Define the function `read_word_list` in the file `wordlist.c` to
match the prototype in `wordle.h`.

You should not assume the length of the list in advance, instead you
should increase the size of the array when needed. Track three
values as you read the array into memory:

1.  The array itself
2.  The number of elements in the array (its length)
3.  The maximum number of elements in the array (its capacity)

Start by picking a reasonable starting capacity (say, 32) and use
`malloc` to allocate an array of that size (remember to multiply the
capacity of the array by the size of each element and give that
total size in bytes to `malloc`).

Each time you read a new word from the file, you should check if
there is room for it in the current array (if the length is less than
the capacity). If not, double the capacity and use `realloc` to
double the size of the underlying array. Use `man realloc` to see
how to use it.

To open a file given its file name, use the `fopen` function:

``` c
FILE *fp = fopen(filename, "r");
```

If it returns `NULL` then something went wrong, but otherwise it is
ready to use. Note that you do not need to know anything about the
structure of a `FILE` object, you just need to keep track of the
pointer to it. To read a single line, use something like:

``` c
char line[16];
if (fgets(line, 16, fp) == NULL) { /* something went wrong */ }
```

`fgets` gets a line of text from `fp`, up to 16 bytes total and
stores it in `line`. It returns `NULL` if there is an error or if
you have reached the end of the file. You may assume that it
indicates the end of file and use that as your signal to stop
reading.

You should verify that the line is exactly 5 letters plus a newline
character (and report an error otherwise). Because it is storing
data in the `line` array and you will keep re-using that array to
read new lines, you must allocate space for each word using
`malloc`. Be sure to allocate enough space for the word (WITHOUT the
trailing newline character) and a terminating null character. You
can copy the word into place using `strcpy` (see the man page for
details).

When you reach the end of the file, you should add one more entry to
the end of the array (make sure that you save room for one extra
entry). Use a `NULL` pointer to mark the end of the array, similar
to how a null character marks the end of a string.

Close the file using `fclose(fp)` when you are finished with it and
before you return. Return the pointer to the beginning of the array
of results.


### `free_word_list`

Since `read_word_list` allocates memory dynamically with `malloc`
and `realloc`, you are responsible for returning that memory to the
system using `free` before your code returns. Implement the function
`free_word_list` in the file `word_list.c` as prototyped in
`wordle.h`. It should do the following:

*   Call `free(str)` for each pointer in the array of strings (once
    for each word that you allocated space for using `malloc`).

*   Call `free` one last time on the array itself.

Once it passes all of the tests for correct output, test it again
using:

    make valgrind

This will run it with a memory testing tool that will check if you
correctly freed all of your memory and closed your open file. It
should report no errors before you move on.
