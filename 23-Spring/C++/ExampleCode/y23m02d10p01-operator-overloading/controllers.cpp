#include "functions.h"
#include "Fraction.h"
#include <iostream>
#include <string>

int fraction_calculator(std::istream& is, std::ostream& os) {
  //Fraction accumulator;
  Fraction accumulator(1, 1);
  int done = 0;
  while(!done) {
    os << std::endl
       << "Current value: ";
    display_fraction(is, os, accumulator);
    os << std::endl;
    std::string action = getString(is, os, "Action? ");
    if(action == "add") {
      add(is, os, accumulator);
    } else if(action == "fadd") {
      fadd(is, os, accumulator);
    } else if(action == "sub") {
      sub(is, os, accumulator);
    } else if(action == "mul") {
      mul(is, os, accumulator);
    } else if(action == "div") {
      div(is, os, accumulator);
    } else if(action == "quit") {
      done = 1;
    } else {
      os << "Unknown command. Try add, sub, mul, div, or quit." << std::endl;
    }
  }
  os << std::endl
     << "Final value: ";
  display_fraction(is, os, accumulator);
  os<< std::endl;
  return 0;
}
