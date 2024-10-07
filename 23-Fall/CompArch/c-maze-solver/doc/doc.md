Maze solver
-----------

In this assignment you will implement a simple maze solver as well
as code to print out mazes. We will start with `print_maze`.


### Print

The maze is represented as a 2-dimensional array. The dimensions of
the array (the X size and Y size) are defined in `solve.h` and are
constants. `main` creates an array and reads a maze in from standard
in, and the maze is reprsented using one `char` value per square.
Here is a simple example maze:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
....@.....@.@.@.@.....@.....@.@
@@@.@.@@@@@.@.@.@@@.@@@.@@@@@.@
@.@.@.........@.....@.....@...@
@.@.@@@@@.@.@@@.@.@@@@@.@@@.@@@
@.@.@.....@.....@.@.@.@...@...@
@.@.@@@@@.@@@.@@@@@.@.@.@@@.@@@
@.....@.@...@...@...........@.@
@.@.@@@.@.@@@@@@@@@.@@@@@.@@@.@
@.@.@.@.....@.@.@.......@.....@
@.@@@.@.@@@@@.@.@.@@@@@@@.@@@.@
@.....@.@...............@.@...@
@.@.@.@.@.@.@.@.@.@.@@@.@@@.@@@
@.@.@.....@.@.@.@.@...@.@......
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

A `@` character represents a wall, and a `.` character represents a
path. The maze always starts at the top left and ends at the bottom
right.

In this example maze the size is 31 across and 15 down, so it would
be represented with the array:

``` c
char field[15][31];
```

but you should always use the values `SIZE_Y` and `SIZE_X` as
defined in `solve.h`:

``` c
char field[SIZE_Y][SIZE_X];
```

The `print_maze` function is given the array as its only input, and
it should print the characters out to the screen with a newline at
the end of each row. You can use `printf` for this, or you can use
`putchar`, which is a more specialized function that prints a single
character (run `man putchar` for details).

Once you have defined `print_maze` you can start testing. You will
need to create a stub for `solve_maze`, which just means a function
with the right type signature that does not do anything yet,
something like:

``` c
void solve_maze(char field[SIZE_Y][SIZE_X]) {
    (void) field;
}
```

The `(void) field;` line is just there to satisfy the compiler and
let you test `print_maze`. Once you actually implement `solve_maze`
you can delete that line. To test it you have a few options:

*   Run `make`. It will read the first input, run your code to print
    it, and then try to solve it. The output of the solved maze will
    be incorrect, but that will not be detected until after the
    first call to `print_maze` so it will still let you test that
    function.

*   Build your code using `make a.out` and run it without invoking
    tests. You can redirect one of the sample inputs to it like
    this:

        ./a.out < inputs/1.input

    This says to run `a.out` but instead of having it take input
    from the keyboard, give it input from the file `inputs/1.input`,
    which is one of the text mazes. Linux will feed it input from
    the file as though it was being typed from the keyboard.

*   Build your code as before, but generate a fresh new maze to feed
    to it. I have included a Python program that generates a fresh
    maze each time it is called. It uses a terrible maze algorithm,
    but it works:

        python3 makemaze.py | ./a.out

    This tells the Linux shell to run the `makemaze.py` program and
    to connect its output to the input of `a.out`.


### Solve

To solve the maze we will use a technique from *cellular logic*. The
approach is to look at each position on the field and decide whether
or not to change it based only on the positions immediately
surrounding it.

Here is the big idea of this solver: we will define a simple dead
end as a path that is surrounded on three sides (up, down, left,
right) by walls. A simple dead end can never be part of the solution
to the maze, so we turn it into a wall instead. This may create a
new simple dead end, so we repeat the process until there are no
simple dead ends left on the maze. What is left is a field of all
walls except for the solution path, which remains intact.

A few important details:

1.  Scan the entire field looking for simple dead ends. Use a pair
    of nested loops to scan every position on the board.

2.  Do not scan the top, bottom, left, or right walls, i.e., confine
    your loops to starting at 1 and ending at one less than the
    size, i.e., `y < SIZE_Y-1` or something similar. This will allow
    you to safely look up, down, left, and right without having to
    worry about checking invalid positions (like `field[-1][2]`).

3.  At each position, check if:

    a)  The position is a path character
    b)  There are exactly three neighbors that are walls

    If so, replace the path with a wall.

4.  After completing a sweep over the entire field (except the very
    edges as noted above), start over if you made any changes.

5.  Return when you have made a complete pass over the field and not
    made any changes.

With each pass over the field, the dead ends will get shorter and
shorter until eventually there are none left.

To test, you might find it helpful to call `print_maze` at various
times to see if the effect is working. For example, make only a
single pass over the field and then call `print_maze`. Look at the
results and see if the dead ends are getting shorter. Be sure to
remove debugging code before you finish.

You will probably want to test this by calling it directly as
described earlier so you can see the complete output even when it is
incorrect. Once you are confident everything is working, run `make`
to get the full test results, and then move on to `grind grade` to
submit your code for grading.
