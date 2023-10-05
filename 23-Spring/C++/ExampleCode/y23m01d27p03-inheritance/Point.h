#ifndef _POINT_H_
#define _POINT_H_

// class declaration
// header file only
class Point {
public:
  Point(); // default constructor
  Point(const double& x, const double& y);

  double getX() const;
  double getY() const;
  void setX(const double& x);
  void setY(const double& y);
  
private:
  double mX;
  double mY;
};
   
#endif /* _POINT_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
