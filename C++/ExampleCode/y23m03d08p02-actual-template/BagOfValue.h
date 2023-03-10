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


#endif /* _BAGOFVALUE_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
