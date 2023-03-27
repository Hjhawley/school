#include "functions.h"
#include <string>

int minimum(int x, int y) {
  int z;
  if(x < y) {
    z = x;
  } else {
    z = y;
  }
  return z;
}

double minimum(double x, double y) {
  double z;
  if(x < y) {
    z = x;
  } else {
    z = y;
  }
  return z;
}

std::string minimum(std::string x, std::string y) {
  std::string z;
  if(x < y) {
    z = x;
  } else {
    z = y;
  }
  return z;
}

