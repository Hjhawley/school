#include <iostream>
#include <vector>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of STL use of exceptions.
 */

int main( ) {
  std::vector<int> x( 5 );
  unsigned int i;
  try {
    std::cout << "Try to run code that may throw an exception." << std::endl;
    for( i = 0; i <= x.size( ); i++) {
      //       ---^^---------
      x[ i ] = i;
    }
    std::cout << "After [] problem." << std::endl;
    for( i = 0; i <= x.size( ); i++) {
      //       ---^^---------
      x.at( i ) = i;
    }
    std::cout << "After at() problem." << std::endl;
  } catch ( std::exception& e ) {
      std::cout << "Exception caught: " << e.what( ) << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  return 0;
}
