#ifndef _PRIMEHUNTER_H_
#define _PRIMEHUNTER_H_

#include <vector>
#include <mutex>

class PrimeHunter {
public:
  void fill_tasks(int max);
  void find_primes();
  void count_many_primes();
  int get_count() const;
protected:
  std::vector<int> possible_primes;
  std::mutex vector_lock;

  int count;
  std::mutex count_lock;
};


#endif /* _PRIMEHUNTER_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
