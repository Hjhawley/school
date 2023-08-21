#include "Point.h"

// this is the incorrect way to initialize data members in the constructor
// Point::Point(double x, double y) {
//   mX = x;
//   mY = y;
// }

Point::Point()
  : mX(0.0), mY(0.0) {
}

Point::Point(const double& x, const double& y)
  : mX(x), mY(y) {
}

double Point::getX() const {
  //return this->mX;
  return mX;
}

double Point::getY() const {
  return mY;
}

void Point::setX(const double& x) {
  mX = x;
}

void Point::setY(const double& y) {
  mY = y;
}
