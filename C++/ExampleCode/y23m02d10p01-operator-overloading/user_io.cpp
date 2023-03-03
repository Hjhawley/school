#include "functions.h"
#include <iostream>
#include <string>

int getInteger(std::istream& is, std::ostream& os, const std::string& prompt) {
  int a;
  os << prompt;
  is >> a;
  return a;
}

std::string getString(std::istream& is, std::ostream& os, const std::string& prompt) {
  std::string a;
  os << prompt;
  is >> a;
  return a;
}

Fraction getFraction(std::istream& is, std::ostream& os, const std::string& prompt) {
  Fraction a;
  os << prompt;
  is >> a; /* std::istream::operator>>(Fraction& f);
              std::istream& operator>>(std::istream&, Fraction& f);
            */
  return a;
}
