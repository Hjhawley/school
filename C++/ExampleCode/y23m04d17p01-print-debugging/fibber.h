#ifndef _FIBBER_H_
#define _FIBBER_H_
#include <vector>

typedef long long int bigint;
bigint fib(bigint n);
bigint fib_memo(bigint n, std::vector<bigint>& memo);

#endif /* _FIBBER_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
