#include "MyVector.h"

#include <iostream>

int main() {
  MyVector v;
  v.resize(10);
  v[0] = 7;
  v[4] = 9;
  v[9] = 13;

  int i;
  for(i = 30; i < 10000000; i*=2) {
    MyVector w;
    w.resize(i);
    v.resize(i);
    // compiler automatically calls destructor on w here.
  }
  v[99] = 12321;

  int x = v[9];

  std::cout << x << std::endl;
  // compiler automatically calls destructor on v here.
  return 0;
}
