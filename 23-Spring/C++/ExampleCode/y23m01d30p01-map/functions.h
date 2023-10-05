#ifndef _FUNCTIONS_H_
#define _FUNCTIONS_H_

#include <map>
#include <string>

void initialize_primes(std::map<std::string, int>& primes);
void add_prime(std::map<std::string, int>& primes, const std::string& name, const int& prime);
void show_primes(const std::map<std::string, int>& primes);
void show_one_prime(std::map<std::string, int>& primes, const std::string& name);
void show_one_prime_safe(std::map<std::string, int>& primes, const std::string& name);

#endif /* _FUNCTIONS_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
