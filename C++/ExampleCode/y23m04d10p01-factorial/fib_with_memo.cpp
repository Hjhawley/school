#include <iostream>
#include <sstream>
#include <vector>

typedef unsigned long long int bigint;

// memoization

bigint fib_with_memo(bigint n, std::vector<bigint>& memo) {
  bigint result;
  if(memo[n] != 0) {
    result = memo[n];
  } else {
    if(n <= 2) {
      result = 1;
    } else {
      result = fib_with_memo(n-1, memo) + fib_with_memo(n-2, memo);
    }
    memo[n] = result;
  }
  return result;
}

int main(int argc, char *argv[]) {
  // std::cout << "sizeof(bigint): " << sizeof(bigint) << std::endl;
  int n = 10;
  if(argc > 1) {
    std::stringstream ss;
    ss.str(argv[1]);
    ss >> n;
    if(!ss.eof()) {
      std::cerr << "usage: " << argv[0] << " n" << std::endl;
      return 1;
    }
  }

  std::vector<bigint> memo(n+1, 0);
  
  bigint f = fib_with_memo(n, memo);
  std::cout << "fib(" << n << ") = " << f << std::endl;
  
  return 0;
}
