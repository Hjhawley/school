/* Family tree data */
/* Do not modify */

parent(shmi,vader).
parent(ruweee,padme).
parent(jobal,padme).
parent(vader,luke).
parent(vader,leia).
parent(padme,luke).
parent(padme,leia).
parent(luke,ben).
parent(mara,ben).
parent(leia,jaina).
parent(leia,jacen).
parent(leia,anakin).
parent(han,jaina).
parent(han,jacen).
parent(han,anakin).

/* Write your code here */

/* male and female facts */
male(ruweee).
male(vader).
male(luke).
male(han).
male(ben).
male(jacen).
male(anakin).

female(shmi).
female(jobal).
female(padme).
female(mara).
female(leia).
female(jaina).

mother(X, Y) :-
    female(X),
    parent(X, Y).

father(X, Y) :-
    male(X),
    parent(X, Y).

sister(X, Y) :-
    female(X),
    parent(P, X),
    parent(P, Y),
    X \= Y.

grandson(X, Y) :-
    male(X),
    parent(P, X),
    parent(Y, P).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

firstCousin(X, Y) :-
    parent(A, X),
    parent(B, Y),
    sibling(A, B),
    X \= Y,
    \+ sibling(X, Y).

descendent(X, Y) :-
    parent(Y, X).

descendent(X, Y) :-
    parent(Y, Z),
    descendent(X, Z).
