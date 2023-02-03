#include "calculator.h"
#include <string>
#include <map>

std::string getString(std::istream& is, std::ostream& os, const std::string& prompt) {
  std::string answer;
  os << prompt;
  is >> answer;
  return answer;
}

int getInteger(std::istream& is, std::ostream& os, const std::string& prompt) {
  int answer;
  os << prompt;
  is >> answer;
  return answer;
}

int calculator(std::istream& is, std::ostream& os) {
  std::map<std::string, CalcFunction> actions;
  CalcFunction calc;
  actions["add"] = add;
  actions["subtract"] = subtract;
  actions["multiply"] = multiply;
  actions["divide"] = divide;
  actions["quit"] = quit;
  
  std::string operation;
  int total = 0;
  int right_hand_operand;
  bool done = false;

  while(!done) {
    os << "Current total: " << total << std::endl;

    // Find user's selected function
    operation = getString(is, os, "Action? ");
    if(actions.find(operation) != actions.end()) {
      calc = actions[operation];
    } else {
      calc = 0;
    }

    // Get operand if appropriate
    // quit if appropriate
    if(calc != 0 && operation != "quit") {
      right_hand_operand = getInteger(is, os, "Operand? ");
    } else if(operation == "quit") {
      done = true;
    }
    
    // Execute user's choice of function
    if(calc != 0) {
      total = calc(total, right_hand_operand);
    } else {
      os << "action: " << operation << " is not known." << std::endl;
      os << "try: add, subtract, multiply, divide, or quit." << std::endl;
    }
  }

  os << "Total: " << total << std::endl;
  return total;
}
