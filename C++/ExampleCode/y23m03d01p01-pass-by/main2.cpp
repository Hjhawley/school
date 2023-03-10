#include <iostream>

class X {
public:
  X();
  virtual int getData() const;
  void setData(int data);
protected:
  int mData;
};

class Y: public X {
public:
  Y();
  int getNewData() const;
  void setNewData(int data);
protected:
  int mNewData;
};

X::X()
  : mData(-1) {
}

int X::getData() const {
  return mData;
}

void X::setData(int data) {
  mData = data;
}

Y::Y() 
  : X(), mNewData(-2) {
}

int Y::getNewData() const {
  return mNewData;
}

void Y::setNewData(int data) {
  mNewData = data;
}


void by_copy(X y) {
  std::cout << y.getData() << std::endl;
  std::cout << "by_copy: &y: " << &y << std::endl;

  // Run Time Type Identification
  // RTTI
  Y *yptr = dynamic_cast<Y*>(&y);
  if(yptr != 0) {
    std::cout << yptr->getNewData() << std::endl;
  }
}

void by_reference(X& y) {
  std::cout << y.getData() << std::endl;
  std::cout << "by_reference: &y: " << &y << std::endl;

  // Run Time Type Identification
  // RTTI
  Y *yptr = dynamic_cast<Y*>(&y);
  if(yptr != 0) {
    std::cout << yptr->getNewData() << std::endl;
  }
}

void by_pointer(X *y) {
  std::cout << (*y).getData() << std::endl;
  std::cout << y->getData() << std::endl;
  std::cout << "by_pointer: y: " << y << std::endl;

  // Run Time Type Identification
  // RTTI
  Y *yptr = dynamic_cast<Y*>(y);
  if(yptr != 0) {
    std::cout << yptr->getNewData() << std::endl;
  }
}

int main() {
  X x;
  x.setData(1);

  Y y;
  y.setData(2);
  y.setNewData(3);

  ////
  std::cout << "&x: " << &x << std::endl;
  by_copy(x);
  by_reference(x);
  by_pointer(&x);
  std::cout << std::endl;
  std::cout << std::endl;
  std::cout << std::endl;

  ////
  std::cout << "&y: " << &y << std::endl;
  by_copy(y);
  by_reference(y);
  by_pointer(&y);

  return 0;
}
