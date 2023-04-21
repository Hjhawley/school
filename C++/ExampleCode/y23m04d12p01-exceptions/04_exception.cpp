#include <iostream>
#include <cstdlib>
#include <ctime>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of thrown exceptions passing up call stack.
 */

int risky_function() {
  int r = std::rand( ) % 5;
  if( r == 0 ) {
    throw 22;
  } else if( r == 1 ) {
    throw 20.1;
  }
  return r;
}

int safe_function_is_it_really() {
  int a = risky_function();
  int b = risky_function();
  return a + b;
}

int main( ) {
  std::srand( std::time( 0 ) );
  int x = 0;
  try {
    std::cout << "Try to run code that may throw an exception." << std::endl;
    x = safe_function_is_it_really();
    std::cout << "After safe_function." << std::endl;
  } catch ( int e ) {
    std::cout << "Int exception caught: " << e << std::endl;
  } catch ( double e ) {
    std::cout << "Double exception caught: " << e << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  std::cout << "x = " << x << std::endl;
  return 0;
}
