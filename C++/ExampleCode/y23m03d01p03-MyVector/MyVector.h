#ifndef _MYVECTOR_H_
#define _MYVECTOR_H_

class MyVector {
public:
  MyVector();
  ~MyVector(); // destructor
  void resize(const int& size);
  int& operator[](const int& index);
private:
  int *mData;
  int mSize;
};

#endif /* _MYVECTOR_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
