#ifndef _PRIMEHUNTER_H_
#define _PRIMEHUNTER_H_

#include <vector>
#include <mutex>

class PrimeHunter {
public:
  PrimeHunter();
  void populate_tasks(const int& max);
  void process_tasks();
  void find_primes_worker();
  std::vector<int>& get_primes();
private:
  std::vector<int> m_task_list;
  std::mutex m_task_lock;
  std::vector<int> m_primes;
  std::mutex m_prime_lock;
};

#endif /* _PRIMEHUNTER_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
