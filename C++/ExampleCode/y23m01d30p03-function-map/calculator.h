#ifndef _CALCULATOR_H_
#define _CALCULATOR_H_
#include <iostream>
#include <string>

std::string getString(std::istream& is, std::ostream& os, const std::string& prompt);

int calculator(std::istream& is, std::ostream& os);

typedef int (*CalcFunction)(const int&, const int&);

int add(const int& a, const int& b);
int subtract(const int& a, const int& b);
int multiply(const int& a, const int& b);
int divide(const int& a, const int& b);
int quit(const int& a, const int& b);

#endif /* _CALCULATOR_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
