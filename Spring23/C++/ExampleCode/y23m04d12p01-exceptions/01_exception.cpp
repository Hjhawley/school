#include <iostream>
#include <ctime>
#include <cstdlib>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of try/catch.
 */

int main( ) {
  std::srand(std::time(0));
  try {
    std::cout << "Try to run code that may throw an exception." << std::endl;
    
    int r = std::rand() % 2;
    
    std::cout << "About to throw exception." << std::endl;
    
    if(r == 0) {
      throw 22;
    }
    std::cout << "Exception not thrown." << std::endl;
  } catch (int e) {
    std::cout << "Exception caught: " << e << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  return 0;
}

/* Possible outputs:
 * if r == 0:
 * Try to run code that may throw an exception.
 * About to throw exception.
 * Exception caught: 22
 * After try/catch.
 *
 * if r != 0:
 * Try to run code that may throw an exception.
 * About to throw exception.
 * After throw.
 * After try/catch.
 *
 */
