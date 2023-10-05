#include "PtrBag.h"

PtrBag::PtrBag()
  : mPtr(0) {
}

PtrBag::~PtrBag() {
  if(mPtr != 0) {
    delete mPtr;
    mPtr = 0;
  }
}

void PtrBag::setData(Data *p) {
  if(mPtr != 0) {
    delete mPtr;
    mPtr = 0;
  }
  mPtr = p;
}

Data& PtrBag::getData() {
  return *mPtr;
}

const Data& PtrBag::getData() const {
  return *mPtr;
}

