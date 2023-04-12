#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <sstream>
#include <mutex>

/*
 * Double threaded
 *    10,000 ->  seconds
 *   100,000 ->  seconds
 * 1,000,000 ->  seconds
 */

int is_prime(int x) {
  int i;
  for(i = 2; i < x; i++) {
    if(x % i == 0) {
      return 0;
    }
  }
  return 1;
}

void count_many_primes(const int& first, const int& last, int& count, std::mutex& count_lock) {

  int i;
  for(i = first; i < last; i++) {
    if(is_prime(i)) {
      count_lock.lock();
      count++;
      count_lock.unlock();
    }
  }
  return;
}


int main(int argc, char **argv) {
  int max_number = 10;
  if(argc > 1) {
    std::stringstream ss;
    ss.str(argv[1]);
    ss >> max_number;
  }

  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  int count = 0;
  std::mutex count_lock;

  std::vector<std::thread> threads;

  /* create threads */
  threads.push_back(std::thread(count_many_primes, 2, max_number/2, std::ref(count), std::ref(count_lock)));
  threads.push_back(std::thread(count_many_primes, max_number/2, max_number, std::ref(count), std::ref(count_lock)));

  /* destroy threads */
  threads[0].join();
  threads[1].join();
  
  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);

  std::cout << count << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
