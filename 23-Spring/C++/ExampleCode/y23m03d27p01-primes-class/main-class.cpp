#include <iostream>
#include <chrono>
#include <vector>
#include <sstream>

#include "PrimeHunter.h"


int main(int argc, char **argv) {
  int max_number = 10;
  if(argc > 1) {
    std::stringstream ss;
    ss.str(argv[1]);
    ss >> max_number;
  }

  PrimeHunter hunter;
  hunter.fill_tasks(max_number);

  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  hunter.find_primes();
  
  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);

  std::cout << hunter.get_count() << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
