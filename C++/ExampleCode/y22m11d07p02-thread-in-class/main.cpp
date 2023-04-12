#include <iostream>
#include <cstdlib>
#include <thread>
#include <vector>
#include <chrono>
#include <sstream>
#include "prime_utils.h"
#include "PrimeHunter.h"

int main(int argc, char **argv) {
  int max = 10;
  if(argc > 1) {
    std::stringstream ss;
    ss.str(argv[1]);
    ss >> max;
  }

  PrimeHunter prime_hunter;
  prime_hunter.populate_tasks(max);

  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  prime_hunter.process_tasks();
  
  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);
  
  std::cout << prime_hunter.get_primes().size() << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
