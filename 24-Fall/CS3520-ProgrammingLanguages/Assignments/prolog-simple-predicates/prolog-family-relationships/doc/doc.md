Prolog: family relationships
============================

**Do not use any library predicates other than those defined and/or
described in lectures or in the textbook. If you need help
understanding how these problems work, talk to me. Looking up
solutions to these problems on the web is cheating, even if you do
not copy the code that you found.**


Family relationships
--------------------

You are provided with a list of `parent(X,Y)` facts. Add `male(X)`
and `female(X)` facts:

* Males: ruweee, vader, luke, han, ben, jacen, anakin
* Females: shmi, jobal, padme, mara, leia, jaina

Define your answers to the following problems in terms of the base
relations `parent(X,Y)`, `female(X)`, and `male(X)`. Your code will
be tested against the specific set of parent facts you are given
(along with the male female facts you add), but your solutions
should be general enough to work with any data set.

1.  Define a `mother` predicate so that `mother(X,Y)` says that `X`
    is the mother of `Y`.

2.  Define a `father` predicate so that `father(X,Y)` says that `X`
    is the father of `Y`.

3.  Define a `sister` predicate so that `sister(X,Y)` says that `X`
    is a sister of `Y`. Be careful, a person cannot be her own
    sister.

4.  Define a `grandson` predicate so that `grandson(X,Y)` says that
    `X` is a grandson of `Y`.

5.  Define the `firstCousin` predicate so that `firstCousin(X,Y)`
    says that `X` is a first cousin of `Y`. Be careful, a person
    cannot be his or her own cousin, nor can a brother or sister
    also be a cousin.

6.  Define a `descendent` predicate so that `descendent(X,Y)` says
    that `X` is a descendent of `Y`.
