#include "Data.h"
#include <iostream>

Data::Data(const int& x)
  : mX(x) {
}

Data::~Data() {
  std::cout << "Goodbye data! " << mX << std::endl;
  mX = -1;
}

void Data::setX(const int& x) {
  mX = x;
}

BigData::BigData(const int& x, const int& y) 
  : Data(x), mY(y) {
}

BigData::~BigData() {
  std::cout << "Goodbye big data! " << mX << " " << mY << std::endl;
  mY = -2;
}

void BigData::setY(const int& y) {
  mY = y;
}
