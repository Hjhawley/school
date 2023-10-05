#include "Point3D.h"

Point3D::Point3D()
  : Point(), mZ(0.0) {
}

Point3D::Point3D(const double& x, const double& y,
                 const double& z)
  : Point(x, y), mZ(z) {
}

double Point3D::getZ() const {
  return mZ;
}

void Point3D::setZ(const double& z) {
  mZ = z;
}
