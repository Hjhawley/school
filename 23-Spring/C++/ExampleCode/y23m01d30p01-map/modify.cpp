#include "functions.h"
#include <map>
#include <string>

void initialize_primes(std::map<std::string, int>& primes) {
  // Several students need to give their favorite prime here
  //primes[std::string] = int;
  //primes[""] = -1;
  primes["Curtis"] = 13;
  primes["Keaton"] = 7;
  primes["Gabe"] = 29;
  primes["Alex"] = 2;
  primes["Jarod"] = (1 << 31) - 1;
}

void add_prime(std::map<std::string, int>& primes, const std::string& name, const int& prime) {
  primes[name] = prime;
}
