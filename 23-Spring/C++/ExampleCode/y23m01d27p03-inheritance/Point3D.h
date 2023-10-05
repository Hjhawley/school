#ifndef _POINT3D_H_
#define _POINT3D_H_

#include "Point.h"

class Point3D: public Point {
public:
  Point3D();
  Point3D(const double& x, const double& y, const double& z);

  double getZ() const;
  void setZ(const double& z);

private:
  double mZ;
  
};

#endif /* _POINT3D_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
