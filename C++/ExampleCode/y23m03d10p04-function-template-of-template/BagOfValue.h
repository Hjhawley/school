#ifndef _BAGOFVALUE_H_
#define _BAGOFVALUE_H_

template <class T>
class BagOfValue {
public:
  BagOfValue();
  ~BagOfValue();
  void push_back(T);
  const T& operator[](int) const;
  T& operator[](int);
  bool operator<(const BagOfValue& rhs) const;
private:
  T *mPtr;
  int mSize;
};

template <class T>
BagOfValue<T>::BagOfValue()
  : mPtr(0), mSize(0) {
}

template <class T>
BagOfValue<T>::~BagOfValue() {
  if(mPtr != 0) {
    delete [] mPtr;
    mPtr = 0;
  }
}

template <class T>
void BagOfValue<T>::push_back(T value) {
  // new space
  T *ptr = new T[mSize + 1];

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

template <class T>
const T& BagOfValue<T>::operator[](int index) const {
  return mPtr[index];
}

template <class T>
T& BagOfValue<T>::operator[](int index) {
  return mPtr[index];
}

template <class T>
bool BagOfValue<T>::operator<(const BagOfValue& rhs) const {
  bool z = false;
  int i;
  for(i = 0; i < mSize; i++) {
    if(i >= rhs.mSize) {
      // rhs ran out, it is smaller
      z = false;
      break;
    }
    if(mPtr[i] < rhs.mPtr[i]) {
      z = true;
      break;
    } else if(mPtr[i] > rhs.mPtr[i]) {
      z = false;
      break;
    }
  }
  if(i == mSize) {
    z = false;
  }
  return z;
}


#endif /* _BAGOFVALUE_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
