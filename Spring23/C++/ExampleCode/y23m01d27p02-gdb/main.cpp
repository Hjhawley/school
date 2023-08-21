#include <iostream>

void set_to_prime(int& x) {
  x = 6;
}

void display_prime(const int& x) {
  std::cout << x << " is prime." << std::endl;
}

int main() {

  int i = 4;
  std::cout << "main: " << "i: " << i << std::endl;
  
  set_to_prime(i);
  std::cout << "main: " << "i after set to prime: " << i << std::endl;

  display_prime(i);
  std::cout << "main: " << "i after display prime: " << i << std::endl;
  
  return 0;
}
