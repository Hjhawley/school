Implementing let bindings
=========================

Please refer to the "Evaluating Local Binding" section of the
"Evaluation" chapter in the book.

Your task is to update the interpreter to understand let bindings
using syntax like the following examples:

    let a = 3 { a + 8 }

    let b = if true { 9 } else { 2 } { b + 1 }

`main.rs` already contains the needed updates and you should not
change it:

*   It refers to the interpreter as `interp` instead of `calc` to
    reflect the change from the textbook. The `calc.rs` file has
    also been renamed to `interp.rs` and all references to `calc`
    updated.

*   A type `Env` has been defined as an alias for the type:

        std::collections::HashMap<String, Value>

    i.e., a hash map (like a Python dictionary) where keys are of
    type String and values are of type Value. `interp` has also been
    updated to accept an environment as a parameter.

*   The `Exp` type has a `Let1` variant that embeds the appropriate
    components.


Tokenizer and parser
--------------------

Start by updating the parser and tokenizer. The tokenizer should add
the following:

*   An `Equal` token that is a single `=` sign
*   A `Let` token that is the word `let`
*   A `Symbol` token that embeds a `String`. Note that the tokenizer
    already parses out words that look like identifiers, but if it
    does not match them to a known reserved word it returns an
    error. Change that to return all unknown words as `Symbol`
    tokens.

The parser already has comments with the updated grammar. Update the
code to parse a `Let1` expression. I suggest using the parser for
conditional expressions as a model.

Note: when you find and use a symbol token, you will need to clone
the string that it contains. The original String will still be part
of the token list, so you will need a copy to use as part of the
expression tree. You can use:

    let cloned_s = s.clone();

or something similar to accomplish this. We did not have to do this
for numbers and booleans because they have a trait that lets them be
cloned automatically. Strings require an explicit clone.


Interpreter
-----------

To implement variable lookup, add a helper function called `lookup`
to mimic the structure outlined in the textbook. Look up how to use
`HashMap` in the documentation or elsewhere.

Note: you will need to clone the value of the variable, similar to
how you needed to clone the string while parsing. This is because
the original value will still be part of the AST, but you will need
a fresh copy to return as the result. Note that in `main.rs` the
`Value` type uses `derive` to automatically implement the ability to
clone a `Value`.

When making a new environment that you can change, clone the old one
(this is not a perfect solution but it is simple) so that you can
make changes to the clone while leaving the original unchanged.
