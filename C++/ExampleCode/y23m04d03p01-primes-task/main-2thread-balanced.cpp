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

void count_many_primes(std::vector<int>& possible_primes, int& count, std::mutex& vector_lock, std::mutex& count_lock) {

  bool done = false;
  int x;
  while(!done) {

    vector_lock.lock();
    if(possible_primes.size() > 0) {
      x = possible_primes.back();
      possible_primes.pop_back();
    } else {
      done = true;
    }
    vector_lock.unlock();
    
    if(!done && is_prime(x)) {
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

  std::vector<int> possible_primes;
  int i;
  for(i = 2; i <= max_number; i++) {
    possible_primes.push_back(i);
  }

  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  int count = 0;
  std::mutex count_lock;
  std::mutex vector_lock;

  std::vector<std::thread> threads;
  unsigned int max_threads = std::thread::hardware_concurrency();
  unsigned int t;


  /* create threads */
  for(t = 0; t < max_threads; t++) {
    threads.push_back(std::thread(count_many_primes, std::ref(possible_primes), std::ref(count), std::ref(vector_lock), std::ref(count_lock)));
  }

  /* destroy threads */
  for(t = 0; t < threads.size(); t++) {
    threads[t].join();
  }
  
  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);

  std::cout << count << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
