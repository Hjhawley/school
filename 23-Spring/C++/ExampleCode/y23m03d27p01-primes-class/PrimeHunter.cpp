#include "PrimeHunter.h"
#include "prime_utils.h"
#include <thread>


void PrimeHunter::fill_tasks(int max_number) {
  int i;
  for(i = 2; i <= max_number; i++) {
    possible_primes.push_back(i);
  }
}

void PrimeHunter::find_primes() {

  std::vector<std::thread> threads;
  unsigned int max_threads = std::thread::hardware_concurrency();
  unsigned int t;
  count = 0;
  
  /* create threads */
  for(t = 0; t < max_threads; t++) {
    // this->count_many_primes()
    threads.push_back(std::thread(&PrimeHunter::count_many_primes, this));
  }

  /* destroy threads */
  for(t = 0; t < threads.size(); t++) {
    threads[t].join();
  }
}

void PrimeHunter::count_many_primes() {
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

int PrimeHunter::get_count() const {
  return count;
}

