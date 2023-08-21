#include "functions.h"
#include <iostream>
#include <string>

int getInteger(std::istream& is, std::ostream& os, const std::string& prompt) {
  int a;
  os << prompt;
  is >> a;
  return a;
}
