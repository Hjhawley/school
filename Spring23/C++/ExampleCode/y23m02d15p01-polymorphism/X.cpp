#include "X.h"

X::X() : mData1(1), mData2(3.14), mData3(false) {
}

void X::setData1(const int& v) {
  if(v > mData1) {
    mData1 = v;
  }
}
void X::setData2(const double& v) {
  if(v < 0) {
    mData2 = v;
  }
}
void X::setData3(const bool& v) {
  mData3 = v;
}


int X::getData1() const {
  return mData1;
}

double X::getValue() const {
  double r = 0.0;
  if(mData3) {
    r = mData1 * mData2;
  } else {
    r = mData2 * mData2;
  }
  return r;
}

