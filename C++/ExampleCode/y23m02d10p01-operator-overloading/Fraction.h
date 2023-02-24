#ifndef _FRACTION_H_
#define _FRACTION_H_
#include <iostream>

class Fraction {
public:
  Fraction(); // initialize to 1/1
  Fraction(const int& numerator, const int& denominator);

  int getNumerator() const;
  int getDenominator() const;

  void setNumerator(const int& n);
  void setDenominator(const int& d);
  
  void add(const int& addend);
  void subtract(const int& subtrahend);
  void multiply(const int& multiplier);
  void divide(const int& divisor);

  Fraction& operator+=(const int& rhs);
  Fraction& operator+=(const Fraction& rhs);

private:
  int mNumerator;
  int mDenominator;
}; // <------ DON'T FORGET THIS SEMICOLON

std::istream& operator>>(std::istream&, Fraction& f);

#endif /* _FRACTION_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
