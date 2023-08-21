#include <iostream>
#include <sstream>
#include <vector>

typedef unsigned long long int bigint;

bigint fib_with_loop(bigint n) {
  bigint result;
  std::vector<bigint> results(n+1);
  unsigned int i;
  results[1] = 1;
  results[2] = 1;
  for(i = 3; i <= n; i++) {
    results[i] = results[i-1] + results[i-2];
  }
  result = results[n];
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
  
  bigint f = fib_with_loop(n);
  std::cout << "fib(" << n << ") = " << f << std::endl;
  
  return 0;
}
