#ifndef _X_H_
#define _X_H_

class X {
public:
  X();

  void setData1(const int& v);
  void setData2(const double& v);
  void setData3(const bool& v);
  
  int getData1() const;

  virtual double getValue() const;
protected:
  int mData1;
  double mData2;
  bool mData3;
};


#endif /* _X_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
