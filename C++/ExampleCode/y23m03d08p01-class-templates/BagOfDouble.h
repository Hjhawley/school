#ifndef _BAGOFDOUBLE_H_
#define _BAGOFDOUBLE_H_

class BagOfDouble {
public:
  BagOfDouble();
  BagOfDouble(const BagOfDouble&);
  ~BagOfDouble();
  int size() const;
  void push_back(double);
  const double& operator[](int) const;
  double& operator[](int);
private:
  double *mPtr;
  int mSize;
};

#endif /* _BAGOFDOUBLE_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
