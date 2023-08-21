#ifndef _FRACTION_H_
#define _FRACTION_H_

class Fraction {
public:
  Fraction(); // initialize to 1/1
  Fraction(const int& numerator, const int& denominator);

  int getNumerator() const;
  int getDenominator() const;
  
  void add(const int& addend);
  void subtract(const int& subtrahend);
  void multiply(const int& multiplier);
  void divide(const int& divisor);


private:
  int mNumerator;
  int mDenominator;
}; // <------ DON'T FORGET THIS SEMICOLON


#endif /* _FRACTION_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
