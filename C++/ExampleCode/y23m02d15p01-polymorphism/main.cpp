#include "X.h"
#include "Y.h"
#include <iostream>
int main() {
  X x1;
  x1.setData1(7);
  x1.setData2(6.8);
  x1.setData3(true);
  std::cout << x1.getValue() << std::endl;
  
  Y y1;
  y1.setData1(7);
  y1.setData2(6.8);
  y1.setData3(true);
  std::cout << y1.getValue() << std::endl;

  X *px = &x1;
  Y *py = &y1;

  std::cout << px->getValue() << std::endl;
  std::cout << py->getValue() << std::endl;

  X *pxy = &y1;
  pxy->setData1(11);
  // pxy->setData4(26);
  std::cout << pxy->getValue() << std::endl;


  return 0;
}
