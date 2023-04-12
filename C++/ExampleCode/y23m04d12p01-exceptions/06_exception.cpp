#include <iostream>
#include <cstdlib>
#include <ctime>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of catch(...).
 */

int risky_function( ) {
  int r = std::rand() % 6;
  if( r == 0 ) {
    throw 20;
  } else if( r == 1 ) {
    throw 20.1;
  } else if( r == 2 ) {
    throw "I rolled a 2!";
  }
  return r;
}

int safe_function( ) {
  int a = risky_function( );
  int b = risky_function( );
  return a + b;
}


int main( ) {
  std::srand( std::time( 0 ) );
  int x = 0;
  try {
    std::cout << "Try to run code that may throw an exception." << std::endl;
    x = safe_function( );
    std::cout << "After safe_function." << std::endl;
  } catch ( int e ) {
    std::cout << "Int exception caught: " << e << std::endl;
  } catch ( double e ) {
    std::cout << "Double exception caught: " << e << std::endl;
  } catch (...) {
    std::cout << "Caught an unexpected exception. "
              << __FILE__ << ":" << __LINE__ << std::endl;
    throw;
    }
  std::cout << "After try/catch." << std::endl;
  std::cout << "x = " << x << std::endl;
  return 0;
}
