#include "fibber.h"
#include <iostream>
#include <sstream>

int main(int argc, char *argv[]) {
  std::vector<bigint> memo;
  bigint n = 6;

  if(argc >= 2) {
    std::stringstream arg;
    arg.str(argv[1]);
    arg >> n;
  }
  memo.resize(n+1, -1);
  // bigint f = fib(n);
  bigint f = fib_memo(n, memo);
  std::cout << "fib(" << n << ") = " << f << std::endl;
  return 0;
}
