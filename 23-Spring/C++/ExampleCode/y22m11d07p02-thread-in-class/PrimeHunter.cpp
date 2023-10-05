#include <vector>
#include <thread>
#include "PrimeHunter.h"
#include "prime_utils.h"

PrimeHunter::PrimeHunter() {
}

std::vector<int>& PrimeHunter::get_primes() {
  return m_primes;
}

void PrimeHunter::populate_tasks(const int& max) {
  int j;
  m_task_list.clear();
  for(j = 2; j <= max; j++) {
    m_task_list.push_back(j);
  }
}

void PrimeHunter::process_tasks() {
  std::vector<std::thread> threads;

  unsigned int max_cores = std::thread::hardware_concurrency();
  unsigned int i;

  for(i = 0; i < max_cores-1; i++) {
    try {
      // this->find_primes_worker();
      threads.push_back(std::thread(&PrimeHunter::find_primes_worker, this));
    } catch (...) {
      break;
    }
  }

  for(i = 0; i < threads.size(); i++) {
    threads[i].join();
  }
}

void PrimeHunter::find_primes_worker() {
  std::vector<int> this_workers_tasks;
  std::vector<int> this_workers_primes;
  unsigned int i;
  bool done = false;
  
  while(!done) {
    this_workers_tasks.resize(0);
    this_workers_primes.resize(0);

    m_task_lock.lock();
    if(m_task_list.size() > 0) {
      for(i = 0; i < 128 && m_task_list.size() > 0; i++) {
        int x = m_task_list.back();
        m_task_list.pop_back();
        this_workers_tasks.push_back(x);
      }
    } else {
      done = true;
    }
    m_task_lock.unlock();
    
    for(i = 0; i < this_workers_tasks.size(); i++) {
      int n = this_workers_tasks[i];
      if(is_prime(n)) {
        this_workers_primes.push_back(n);
      }
    }

    m_prime_lock.lock();
    for(i = 0; i < this_workers_primes.size(); i++) {
      m_primes.push_back(this_workers_primes[i]);
    }
    m_prime_lock.unlock();

  }
}

