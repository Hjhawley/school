#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <mutex>
#include "ThreadedVector.h"

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

void count_many_primes(ThreadedVector<int>& possible_primes, int& count, std::mutex& count_lock) {
  std::vector<int> my_tasks;
  int i;
  while(possible_primes.size() > 0) {
    my_tasks.clear();
    possible_primes.pop_back(my_tasks, 10);
    unsigned int j;
    for(j = 0; j < my_tasks.size(); j++) {
      i = my_tasks[j];
      if(is_prime(i)) {
        count_lock.lock();
        count++;
        count_lock.unlock();
      }
    }
  }
  
  return;
}


int main() {
  // start time
  std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

  int max_number = 100000;
  int count = 0;
  std::mutex vector_lock;
  std::mutex count_lock;
  ThreadedVector<int> possible_primes;
  int i;
  for(i = 2; i <= max_number; i++) {
    possible_primes.push_back(i);
  }
  std::vector<std::thread> threads;
  int max_threads = std::thread::hardware_concurrency();
  std::cout << "max threads: " << max_threads << std::endl;

  /* create threads */
  for(i = 0; i < max_threads; i++) {
    threads.push_back(std::thread(count_many_primes, std::ref(possible_primes), std::ref(count), std::ref(count_lock)));
  }

  /* destroy threads */
  for(i = 0; i < max_threads; i++) {
    threads[i].join();
  }
  
  // end time
  std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();

  // calculate time span
  std::chrono::duration<double> time_span = 
    std::chrono::duration_cast<std::chrono::duration< double>>(t2 - t1);

  std::cout << count << " primes found in " << time_span.count() << " seconds." << std::endl;
  return 0;
}
