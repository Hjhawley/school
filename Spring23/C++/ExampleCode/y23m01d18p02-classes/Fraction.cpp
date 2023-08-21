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
