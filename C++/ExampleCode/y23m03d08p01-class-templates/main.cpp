#include <iostream>
#include "BagOfInt.h"
#include "BagOfDouble.h"

void show_ints(const BagOfInt& b) {
  int i;
  for(i = 0; i < b.size(); i++) {
    std::cout << i << " " << b[i] << std::endl;
  }
}

int main() {

  BagOfInt primes; // check
  primes.push_back(2); // check
  primes.push_back(3); // check
  primes.push_back(5); //[2] // check
  primes.push_back(7); // check

  show_ints(primes);

  std::cout << primes[2] << std::endl;
  primes[3] = 11;
  std::cout << primes[3] << std::endl;

  BagOfDouble numbers; // check
  numbers.push_back(2.1); // check
  numbers.push_back(3.1); // check
  numbers.push_back(5.1); //[2] // check
  numbers.push_back(7.1); // check

  std::cout << numbers[2] << std::endl;
  numbers[3] = 11.1;
  std::cout << numbers[3] << std::endl;

  return 0;
}

