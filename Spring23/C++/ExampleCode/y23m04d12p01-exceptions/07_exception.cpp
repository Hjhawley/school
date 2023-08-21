#include <iostream>
#include <cstdlib>
#include <ctime>
#include <exception>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of user-defined exceptions.
 */

class myexception: public std::exception {
public:
  myexception(const char *msg_in) {
    msg = msg_in;
  }
  virtual const char* what( ) const throw( ) {
    return this->msg;
  }
private:
  const char *msg;
};


int risky_function( ) {
  int r = std::rand( ) % 6;
  if(r == 0) {
    throw( myexception( "r == 0" ) );
  } else if( r == 1 ) {
    throw( myexception( "r == 1" ) );
  } else if( r == 2 ) {
    throw( myexception( "r == 2" ) );
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
  } catch ( std::exception& e ) {
    std::cout << "Exception caught: " << e.what( ) << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  std::cout << "x = " << x << std::endl;
  return 0;
}
