#include <iostream>
#include "BagOfValue.h"

int main() {

  BagOfValue<int> primes; // check
  primes.push_back(2); // check
  primes.push_back(3); // check
  primes.push_back(5); //[2] // check
  primes.push_back(7); // check

  std::cout << primes[2] << std::endl;
  primes[3] = 11;
  std::cout << primes[3] << std::endl;

  BagOfValuBagOfValue<int>e<double> numbers; // check
  numbers.push_back(2.1); // check
  numbers.push_back(3.1); // check
  numbers.push_back(5.1); //[2] // check
  numbers.push_back(7.1); // check

  std::cout << numbers[2] << std::endl;
  numbers[3] = 11.1;
  std::cout << numbers[3] << std::endl;

  return 0;
}

