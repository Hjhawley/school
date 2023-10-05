#include "prime_utils.h"

bool is_prime(int n) {
  // true, false
  bool result = true;
  int d, r;
  if(n <= 1) {
    result = false;
  }
  else if(n == 2) {
    result = true;
  }
  else if((n % 2) == 0) {
    result = false;
  }
  for(d = 2; d < n && result; d++) {
    r = n % d;
    if(r == 0) {
      result = false;
      break;
    }
  }
  return result;
}

int count_primes(int min, int max) {
  int n;
  int count = 0;
  for(n = min; n <= max; n++) {
    if(is_prime(n)) {
      count++;
    }
  }
  return count;
}
