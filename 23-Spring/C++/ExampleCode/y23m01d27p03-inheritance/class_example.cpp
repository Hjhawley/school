#include "Point.h"
#include "Point3D.h"
#include <iostream>

int main() {
  // type variable(parameters, to, constructor);
  Point p1(1.2, 4.5);
  // type variable; uses default constructor
  Point p2;

  Point3D p3;
  Point3D p4(1.1,2.2,3.3);

  std::cout << p1.getX() << "," << p1.getY()
            << std::endl;

  p1.setX(-423.1);
  p1.setY(821.4);

  std::cout << p1.getX() << "," << p1.getY()
            << std::endl;
  
  std::cout << p4.getX() << "," << p4.getY()
            << "," << p4.getZ()
            << std::endl;
  
  return 0;
}
