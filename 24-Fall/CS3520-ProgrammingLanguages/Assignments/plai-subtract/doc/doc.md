Adding subtraction to the interpreter
=====================================

The starter code for this assignment is the interpreter after adding
booleans (with a few other tweaks). Your job is to add subtraction
to the language.


Changing how minus signs are tokenized
--------------------------------------

The first step is to change how minus signs are tokenized and
parsed. Consider this simple expression:

    1 -5

The tokenizer will currently tokenize this into:

    [Number(1.0), Number(-5.0)]

but it should be equivalent to the expression:

    1 - 5

and tokenized as:

    [Number(1.0), Minus, Number(5.0)]

Run `make` and you should see how `-4` is currently tokenized and
how it is expected to be tokenized going forward. Note that
`main.rs` now prints out the token list and the parsed AST before
evaluating each expression.

Start by adding a new `Token` variant called `Minus` in `parse.rs`.
Then modify the tokenizer to recognize a `-` character as a `Minus`
token (this will be very similar to how `+` is recognized as `Plus`)
and change the number tokenizer so it no longer recognized the `-`
character.

Run `make` to see that it is now tokenized correctly but still
cannot parse it.


Changing how minus signs are parsed
-----------------------------------

Now update the parser. The grammar for terms is given in a comment
in `parse.rs`:

    // term             -> ( expression ) | conditional | number | bool

Change it to be:

    // term             -> ( expression ) | conditional | - number | number | bool

and then update how `parse_term` is implemented to match the change
in the grammar: add a case for the `Minus` token that parses a
number `n` and returns `-n`. This essentially makes `-` a unary
prefix operator (to negate a number), but we handle the negation
directly in the parser.

Run `make` and it should succeed until `-` is used to mean
subtraction.


Adding a Minus expression type
------------------------------

Add a `Minus` expression variant in `main.rs` that mimics the
structure of `Plus`. Update the rest of the parser (including the
grammar definition in the comments) and the evaluator to support the
new expression type.

Note: subtraction should be left associative and have the same
precedence as addition, which will also be the most straightforward
way to implement it.
