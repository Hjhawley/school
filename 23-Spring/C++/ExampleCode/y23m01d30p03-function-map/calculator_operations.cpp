#include "calculator.h"

int add(const int& a, const int& b) {
  return a + b;
}

int subtract(const int& a, const int& b) {
  return a - b;
}

int multiply(const int& a, const int& b) {
  return a * b;
}

int divide(const int& a, const int& b) {
  return a / b;
}

int quit(const int& a, const int& b) {
  (void) b;
  // does not change a
  return a;
}
