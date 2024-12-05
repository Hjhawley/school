Prolog Lists
============

Write your solutions to these problems in the file `lists.pl`.

For these problems, you should not use any other predicates. Each
problems should be a standalone implementation, i.e., no `nth0`,
`select`, or other predicates. You should also avoid any arithmetic
operations.

Try to avoid thinking about the procedure necessary to solve the
problem, and focus on describing the requirements in a declarative
way by relying on unification.

1.  Define a `third` predicate so that `third(X,Y)` says that `Y` is
    the third element of the list `X`. (The predicate should fail if
    `X` has fewer than three elements.) *Hint:* This can be
    expressed as a fact.

2.  Define a `del3` predicate so that `del3(X,Y)` says that the list
    `Y` is the same as the list `X` but with the third element
    deleted. (The predicate should fail if `X` has fewer than three
    elements.) *Hint:* This can be expressed as a fact.

3.  Define a predicate `isDuped` so that `isDuped(Y)` succeeds if
    and only if `Y` is a list of even length where each element in
    the list appears twice in a row. That is, the predicate should
    succeed if and only if the first and second elements are equal,
    and the third and fourth elements are equal, and so on to the
    end of the list. It should fail for all odd-length list.

4.  Define the `evenSize` predicate so that `evenSize(X)` says that
    `X` is a list whose length is an even number. *Hint:* You do not
    need to compute the actual length, or do any integer arithmetic.
