#include <iostream>
#include <sstream>

typedef unsigned long long int bigint;

bigint fact_no_loop(bigint n) {
  bigint result;
  if(n == 1) {
    result = 1;
  } else {
    result = n * fact_no_loop(n-1);
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
  
  bigint f = fact_no_loop(n);
  std::cout << n << "! = " << f << std::endl;
  
  return 0;
}
