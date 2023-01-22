#ifndef _FUNCTIONS_H_
#define _FUNCTIONS_H_
#include "Fraction.h"
#include <iostream>


// user_io.cpp
int getInteger(std::istream& is, std::ostream& os, const std::string& prompt);
std::string getString(std::istream& is, std::ostream& os, const std::string& prompt);

// controllers.cpp
int fraction_calculator(std::istream& is, std::ostream& os);

// actions.cpp
void add(std::istream& is, std::ostream& os, Fraction& f);
void sub(std::istream& is, std::ostream& os, Fraction& f);
void mul(std::istream& is, std::ostream& os, Fraction& f);
void div(std::istream& is, std::ostream& os, Fraction& f);
void display_fraction(std::istream& is, std::ostream& os, Fraction& f);

#endif /* _FUNCTIONS_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
