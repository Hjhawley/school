#include "functions.h"
#include <iostream>

int adder(std::istream& is, std::ostream& os) {
  int a = getInteger(is, os, "Integer1? ");
  int b = getInteger(is, os, "Integer2? ");

  // print("The sum of " + str(a) + " and " + str(b) + " is " + str(a+b) + ".")
  os << "The sum of " << a << " and " << b << " is " << a+b << "." << std::endl;
  return a+b;
}
