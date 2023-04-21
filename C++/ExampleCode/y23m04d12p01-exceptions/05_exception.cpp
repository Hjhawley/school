#include <iostream>
#include <cstdlib>
#include <ctime>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of uncaught exception.
 */

int risky_function( ) {
  int r = std::rand( ) % 6;
  if( r == 0 ) {
    throw 22;               // int
  } else if( r == 1 ) {
    throw 20.1;             // double
  } else if( r == 2 ) {
    //throw "I rolled a 2!";  // string (const char *)
    throw std::string("I rolled a 2!");  // std::string
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
    if(e < 20) {
      std::cout << "Life goes on" << std::endl;
    } else {
      std::cout << "Int exception caught: " << e << std::endl;
    }
  } catch ( double e ) {
    std::cout << "Double exception caught: " << e << std::endl;
  } catch ( std::string e ) {
    std::cout << "std::string exception caught: " << e << std::endl;
  } catch ( const char *e ) {
    std::cout << "C-string exception caught: " << e << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  std::cout << "x = " << x << std::endl;
  return 0;
}
