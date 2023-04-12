#include <iostream>
#include <sstream>

int fact(int n) {
  int i;
  int result = 1;
  for(i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

int main(int argc, char *argv[]) {
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
  
  int f = fact(n);
  std::cout << n << "! = " << f << std::endl;
  
  return 0;
}
