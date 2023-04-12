Exceptions
----------

C++ exceptions are used to handle runtime errors.  Program control
is transferred to exception handlers when these conditions occur.

Basic Syntax
------------

Code that encounters a runtime error may throw an exception
as a signal that something exceptional has occurred.  Each
exception has a type and value.  Exceptions are thrown with
the keyword `throw` followed by a value to be thrown.

Code that may throw an exception should be wrapped in a try
clause.  Try clauses are code blocks preceded by the keyword `try`.

If an exception is thrown in code called by a try clause, it
needs to be caught by a catch clause.  Catch clauses are created
by a block of code following the keyword `catch`, a declaration
of the type of exception to be caught, and a variable to receive
the exception thrown.

Each try must have at least one catch.  Trys may have more than
one catch.  Each catch must catch a different exception type.

See 01_exception.cpp and 02_exception.cpp as simple examples.

Catching Multiple Types
-----------------------

If the code inside the try clause may throw exceptions of
multiple types, then use multiple catch clauses attached
to the same try clause.  The catch with the type matching
the type of the exception thrown will fire and execute.

See 03_exception.cpp as a simple example.

Multi-level Catch
-----------------

It is possible that the execption thrown is multiple
levels of function calls inside the try clause.  If this
is the case, then the exception is passed up the call stack,
until a try clause with a matching catch clause is found.
All of the function calls below the try are removed
from the stack, and execution of the program continues
in the catch clause.

See 04_exception.cpp as a simple example.

Uncaught Exceptions
-------------------

When an exception is thrown, the runtime code finds the
nearest relevant catch clause, and passes control to that
clause.  What if there is no catch clause that matches the
type of the exception?

If the runtime system can not find a handler, then the default
handler (above main()) is found, and the program is 
terminated.

See 05_exception.cpp as a simple example.

Default Handlers
----------------

A default handler can be added with `catch(...)`.  This catches
any uncaught exceptions.  However, the exception itself, is
not available.  Place the default catch after all other
catches in the associated try.  This is mostly useful to let
yourself know that you missed an exception type that should
have been handled.  Be careful not to overuse this clause.
Don't catch an exception unless you know how to handle it.
You can also re-throw an exception after logging it, or
partially handling it.

See 06_exception.cpp as a simple example.


std::exception
--------------

The STL defines a class named `std::exception` that is
intended to organize user-defined exceptions, and
simplify the process of catching exceptions.

To define an exception, inherit from `std::exception`,
and override the method `virtual const char* what() const throw()`.
The `throw()` at the end specifies that the `what()` method should
not throw any exceptions, because the `()` are empty.  If the
method does throw an exception, it will be automatically translated
to the `std::unexpected` exception.

To catch an exception, `catch(std::exception &e)`.  Then,
call `e.what()` to find the actual exception.


See 07_exception.cpp as a simple example.


STL Exceptions
--------------

The STL uses std::exception to define numerous 
exceptions that may occur in C++.  When using
the STL, consider the exceptions that might
occur, and what your code should do in each case.
Use try/catch to produce well-behaved programs.

See 08_exception.cpp as a simple example.
See 09_exception.cpp as another simple example.


Exception Challenges
--------------------
- Write a program that determines the
  largest amount of memory that can be
  allocated.  How will you use exceptions
  to find this?
- Read about one of the STL containers, and
  find exceptions that it may throw.  Create
  conditions to cause the container to throw
  the exception.  Catch the exception.

