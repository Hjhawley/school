#include "PtrBag.h"
#include "Data.h"
#include <iostream>

void other_function(const PtrBag& b) {
  const Data& d = b.getData();
  //...
  std::cout << "Other function is ending." << std::endl;
}

void yaf(PtrBag& b) {
  Data& d = b.getData();
  d.setX(1234);

  BigData *bd = dynamic_cast<BigData *>(&d);
  if(bd != 0) {
    bd->setY(1235);
  }
}

int main() {
  PtrBag b;

  b.setData(new Data(17));
  //...
  b.setData(new Data(23));
  b.getData().setX(29);
  yaf(b);
  //...

  b.setData(new BigData(101, 103));
  yaf(b);
  // ...

  b.setData(new Data(43));

  other_function(b);
  std::cout << "Other function is ended." << std::endl;
  return 0;
}
