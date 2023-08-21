#include "Fraction.h"
#include "functions.h"
#include <iostream>

void add(std::istream& is, std::ostream& os, Fraction& f) {
  int n = getInteger(is, os, "addend: ");
  f += n;
}

void fadd(std::istream& is, std::ostream& os, Fraction& f) {
  Fraction n = getFraction(is, os, "addend as a fraction: ");
  f += n;
}

void sub(std::istream& is, std::ostream& os, Fraction& f) {
  int n = getInteger(is, os, "subtrahend: ");
  f.subtract(n);
}

void mul(std::istream& is, std::ostream& os, Fraction& f) {
  int n = getInteger(is, os, "multiplier: ");
  f.multiply(n);
}

void div(std::istream& is, std::ostream& os, Fraction& f) {
  int n = getInteger(is, os, "divisor: ");
  f.divide(n);
}

void display_fraction(std::istream& is, std::ostream& os, Fraction& f) {
  (void) is; // fake using is
  os << f.getNumerator() << "/" << f.getDenominator();
}
