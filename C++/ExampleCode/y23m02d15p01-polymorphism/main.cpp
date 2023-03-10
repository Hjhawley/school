#include "X.h"
#include "Y.h"
#include <iostream>
int main() {
  X x1;
  x1.setData1(7);
  x1.setData2(6.8);
  x1.setData3(true);
  std::cout << x1.getValue() << std::endl;
  // 21.98
  
  Y y1;
  y1.setData1(7);
  y1.setData2(6.8);
  y1.setData3(true);
  std::cout << y1.getValue() << std::endl;
  // 14

  X *px = &x1;
  Y *py = &y1;

  std::cout << px->getValue() << std::endl;
  // 21.98
  std::cout << py->getValue() << std::endl;
  // 14

  X *pxy = &y1;
  pxy->setData1(11);
  
  // pxy = &x1;

  /*
   * if pxy actually points to a Y object, call setData4
   */
  Y *pyy = dynamic_cast<Y *>(pxy);
  if(pyy != 0) {
    std::cout << "Calling setData4()" << std::endl;
    pyy->setData4(26);
  }


  std::cout << pxy->getValue() << std::endl;
  // 286

  return 0;
}
