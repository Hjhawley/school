#include "BagOfDouble.h"

BagOfDouble::BagOfDouble()
  : mPtr(0), mSize(0) {
}

BagOfDouble::BagOfDouble(const BagOfDouble& rhs)
  : mPtr(0), mSize(0) {
  int i;
  for(i = 0; i < rhs.mSize; i++) {
    push_back(rhs[i]);
  }
}

BagOfDouble::~BagOfDouble() {
  if(mPtr != 0) {
    delete [] mPtr;
    mPtr = 0;
  }
}

int BagOfDouble::size() const {
  return mSize;
}

void BagOfDouble::push_back(double value) {
  // new space
  double *ptr = new double[mSize + 1];

  // copy old values
  int i;
  for(i = 0; i < mSize; i++) {
    ptr[i] = mPtr[i];
  }

  // insert new value
  ptr[mSize] = value;

  // free old memory
  if(mPtr != 0) {
    delete [] mPtr;
  }
  
  // increment size
  mSize++;
  
  // update data member ptr
  mPtr = ptr;
}

const double& BagOfDouble::operator[](int index) const {
  return mPtr[index];
}

double& BagOfDouble::operator[](int index) {
  return mPtr[index];
}
