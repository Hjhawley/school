#include <iostream>
#include <chrono>
#include <sstream>

/*
 * Single threaded
 *     1,000 -> ??? seconds
 *    10,000 -> ??? seconds
 *   100,000 -> ??? seconds
 * 1,000,000 -> ??? seconds
 */

int is_prime_fast_that_you_like(int x) {
  int i;
  if(x == 2) {
    return 1;
  }
  if(x % 2 == 0) {
    return 0;
  }
  for(i = 3; i*i <= x; i += 2) {
    if(x % i == 0) {
      return 0;
    }
  }
  return 1;
}

int is_prime(int x) {
  int i;
  for(i = 2; i < x; i ++) {
    if(x % i == 0) {
      return 0;
    }
  }
  return 1;
}

int main(int argc, char *argv[]) {
  // ./main max
  int max_number = 10;
  if(argc > 1) {
    std::stringstream ss;
    ss.str(argv[1]);
    ss >> max_number;
    if(!ss.eof()) {
      std::cerr << "usage: " << argv[0] << " maximum_number" << std::endl;
      return 1;
    }
  }

  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  int count = 0;
  int i;
  for(i = 2; i <= max_number; i++) {
    if(is_prime(i)) {
      count++;
    }
  }

  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);

  std::cout << count << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
