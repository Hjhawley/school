#ifndef _BAGOFINT_H_
#define _BAGOFINT_H_

class BagOfInt {
public:
  BagOfInt(); // default constructor
  BagOfInt(const BagOfInt&); // copy constructor
  ~BagOfInt();
  int size() const;
  void push_back(int);
  const int& operator[](int) const;
  int& operator[](int);
private:
  int *mPtr;
  int mSize;
};

#endif /* _BAGOFINT_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
