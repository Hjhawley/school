#include "BagOfInt.h"

BagOfInt::BagOfInt()
  : mPtr(0), mSize(0) {
}

BagOfInt::BagOfInt(const BagOfInt& rhs)
  : mPtr(0), mSize(0) {
  int i;
  for(i = 0; i < rhs.mSize; i++) {
    push_back(rhs[i]);
  }
}

BagOfInt::~BagOfInt() {
  if(mPtr != 0) {
    delete [] mPtr;
    mPtr = 0;
  }
}

int BagOfInt::size() const {
  return mSize;
}

void BagOfInt::push_back(int value) {
  // new space
  int *ptr = new int[mSize + 1];

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

const int& BagOfInt::operator[](int index) const {
  return mPtr[index];
}

int& BagOfInt::operator[](int index) {
  return mPtr[index];
}
