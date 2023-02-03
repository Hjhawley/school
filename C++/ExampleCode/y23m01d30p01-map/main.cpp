#include "functions.h"
#include <iostream>
#include <map>
#include <string>

/*
 * https://cplusplus.com/reference/map/map/
 */

int main() {
  std::map<std::string, int> primes;

  initialize_primes(primes);
  add_prime(primes, "Hayden", 5);
  show_primes(primes);

  show_one_prime(primes, "student");
  show_one_prime(primes, "student-other");
  show_one_prime_safe(primes, "yet-student-other");
  return 0;
}
