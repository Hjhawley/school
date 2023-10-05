#include "functions.h"
#include <map>
#include <string>
#include <iostream>

void show_primes(const std::map<std::string, int>& primes) {
  // for key in primes:
  //    print(key, primes[key])

  std::map<std::string, int>::const_iterator p;
  for(p = primes.begin(); p != primes.end(); p++) {
    std::cout << p->first << " " << p->second << std::endl;
  }
}

void show_one_prime(std::map<std::string, int>& primes, const std::string& name) {
  std::cout << name << "'s favorite prime is " << primes[name] << std::endl;
}

void show_one_prime_safe(std::map<std::string, int>& primes, const std::string& name) {
  if(primes.find(name) != primes.end()) {
    std::cout << name << "'s favorite prime is " << primes[name] << std::endl;
  } else {
    std::cout << name << " does not have a favorite prime." << std::endl;
  }
}
