% third(X, Y): Y is the third element of the list X.
third([_, _, Y | _], Y).

% del3(X, Y): Y is the list X with the third element removed.
del3([A, B, _ | T], [A, B | T]).

% isDuped(Y): Y is a list of even length where every two consecutive elements are identical.
isDuped([]).
isDuped([X, X | T]) :-
    isDuped(T).

% evenSize(X): X is a list whose length is an even number.
evenSize([]).
evenSize([_, _ | T]) :-
    evenSize(T).
