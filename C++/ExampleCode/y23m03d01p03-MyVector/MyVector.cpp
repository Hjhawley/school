#include "MyVector.h"

MyVector::MyVector()
  : mData(0), mSize(0) {
  // empty
}

MyVector::~MyVector() {
  if(mData != 0) {
    delete [] mData;
    mData = 0;
    mSize = 0;
  }
}

void MyVector::resize(const int& size) {
  // get new space without forgetting old space yet.
  int *tmp = new int[size];

  // copy old data
  int i;
  int copy_size = size;
  if(mSize < copy_size) {
    copy_size = mSize;
  }
  for(i = 0; i < copy_size; i++) {
    tmp[i] = mData[i];
  }

  // release old space
  delete [] mData;

  // remember new space
  mData = tmp;
  mSize = size;
}

int& MyVector::operator[](const int& index) {
  return *(mData+index);
  //return mData[index];
}
