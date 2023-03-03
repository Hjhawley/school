#include "Fraction.h"

Fraction::Fraction()
  : mNumerator(1), mDenominator(1) {
}
/* please don't do this, even though it appears to work.
Fraction::Fraction() {
  mNumerator = 1;
  mDenominator = 1;
}
*/
Fraction::Fraction(const int& numerator, const int& denominator)
  : mNumerator(numerator), mDenominator(denominator) {
}

int Fraction::getNumerator() const {
  return this->mNumerator;
}
int Fraction::getDenominator() const {
  return mDenominator;
}

void Fraction::setNumerator(const int& n) {
  this->mNumerator = n;
}
void Fraction::setDenominator(const int& d) {
  this->mDenominator = d;
}

void Fraction::add(const int& addend) {
  mNumerator += addend * mDenominator;
}
void Fraction::subtract(const int& subtrahend) {
  //add(-subtrahend);
  //this->add(-subtrahend);
  mNumerator -= subtrahend * mDenominator;
}
void Fraction::multiply(const int& multiplier) {
  mNumerator *= multiplier;
}
void Fraction::divide(const int& divisor) {
  mDenominator *= divisor;
}

Fraction& Fraction::operator+=(const int& rhs) {
  // Fraction *this;
  mNumerator += rhs * mDenominator;
  return *this;
}

Fraction& Fraction::operator+=(const Fraction& rhs) {
  // Fraction *this;
  int d = mDenominator * rhs.mDenominator;
  int n = mNumerator * rhs.mDenominator + rhs.mNumerator * mDenominator;
  mNumerator = n;
  mDenominator = d;
  return *this;
}

/*
void add(Fraction& f, const int& addend) {
  f.mNumerator += addend * f.mDenominator;
}
*/
/*
void dummy() {
  Fraction one;
  Fraction three_halves(3, 2);
  int one = 1;
  int two = 2;
  Fraction one_half(one, two);
}
*/


std::istream& operator>>(std::istream& is, Fraction& f) {
  // numerator/denominator
  int n, d;
  char c;
  is >> n;
  is.read(&c, 1);
  is >> d;
  f.setNumerator(n);
  f.setDenominator(d);
  return is;
}
