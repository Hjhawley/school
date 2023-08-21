#include <iostream>

int main() {
  if(1) {
    std::cout << "BAD!!" << std::endl;
    int *ptr = 0;
    *ptr = 1;
  }
  return 0;
}
