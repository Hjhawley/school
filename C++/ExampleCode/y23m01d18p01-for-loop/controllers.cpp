#include "functions.h"
#include <iostream>

int adder(std::istream& is, std::ostream& os) {
  int a = getInteger(is, os, "Integer1? ");
  int b = getInteger(is, os, "Integer2? ");

  // print("The sum of " + str(a) + " and " + str(b) + " is " + str(a+b) + ".")
  os << "The sum of " << a << " and " << b << " is " << a+b << "." << std::endl;
  return a+b;
}

int guess_my_number(std::istream& is, std::ostream& os) {
  int my_number = 75;
  int your_number = my_number -1;
  int attempt;
  //
  // intialization - once
  // check if condition is true
  //   execute the body of the loop
  //   incrermentation
  //   go to check condition
  //
  // for attempt in range(10):
  // for(initialization; condition; incrementation)
  for(attempt = 0; attempt < 10; attempt++) {
    your_number = getInteger(is, os, "Guess my number: ");
    if(your_number < my_number) {
      os << "Too low." << std::endl;
    } else if(your_number > my_number) {
      os << "Too high." << std::endl;
    } else {
      os << "That's it!" << std::endl;
      break;
    }
  }
  int rvalue;
  if(attempt < 10) {
    os << "Congratulations. You win!" << std::endl;
    rvalue = 0;
  } else {
    os << "Better luck next time." << std::endl;
    rvalue = 1;
  }
  return rvalue;
}
