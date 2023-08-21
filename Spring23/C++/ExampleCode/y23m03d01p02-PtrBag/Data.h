#ifndef _DATA_H_
#define _DATA_H_

class Data {
public:
  Data(const int& x);
  virtual ~Data();
  void setX(const int& x);
  
protected:
  int mX;
};

class BigData : public Data {
public:
  BigData(const int& x, const int& y);
  virtual ~BigData();
  void setY(const int& y);
protected:
  int mY;
};

#endif /* _DATA_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
