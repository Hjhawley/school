#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
  int i, r;
  for(i = 0; i < 10; i++) {
    std::srand(std::time(0)); // OOPS! Same number every time through the loop.
    r = std::rand(); // generate random numbers as often as you want.
    std::cout << i << " " << r << std::endl;
  }
  return 0;
}
