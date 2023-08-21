#ifndef _Y_H_
#define _Y_H_

#include "X.h"

class Y: public X {
public:
  Y();
  double getData2() const;
  void setData4(const int& v);
  virtual double getValue() const;
private:
  int mData4;
};

#endif /* _Y_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
