#include <iostream>
#include <cstdlib>
#include <ctime>

/* Trace the execution path of this code.
 * Can you predict the output before running it?
 *
 * Demonstration of catching multiple exception types.
 */

int risky_function() {
  int r = std::rand() % 6;
  if(r == 0) {
    throw 22;
  } else if(r == 1) {
    throw 9;
  } else if(r == 2) {
    throw 20.1;
  } else if(r == 3) {
    throw 95.9;
  }
  return r;
}

int main( ) {
  std::srand(std::time(0));
  int x = 0;
  try {
    std::cout << "Try to run code that may throw an exception." << std::endl;
    x = risky_function();
    std::cout << "After risky_function." << std::endl;
  } catch (int e) {
    std::cout << "Int exception caught: " << e << std::endl;
  } catch (double e) {
    std::cout << "Double exception caught: " << e << std::endl;
  }
  std::cout << "After try/catch." << std::endl;
  std::cout << "x = " << x << std::endl;
  return 0;
}
