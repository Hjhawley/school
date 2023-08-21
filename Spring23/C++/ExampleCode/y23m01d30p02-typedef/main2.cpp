#include <iostream>

typedef unsigned long long int u_int64;

double multiply(u_int64 a, double b) {
  return a * b;
}

double add(u_int64 a, double b) {
  return a + b;
}



typedef double (*MathFunction)(u_int64, double);


int main() {
  //double (*generic_function_pointer1)(int, double) = multiply;
  //double (*generic_function_pointer2)(int, double) = add;
  MathFunction generic_function_pointer1 = multiply;
  MathFunction generic_function_pointer2 = add;
  double (*g)(u_int64, double) = multiply;

  g = generic_function_pointer1;
  
  double r = generic_function_pointer1(25, 21.22);
  std::cout << "r " << r << std::endl;

  double p = multiply(3, 3.14);
  std::cout << "p " << p << std::endl;

  //double (*times)(int, double) = multiply;
  MathFunction times = multiply;
  
  double q = times(2, 2.71);
  
  std::cout << "q " << q << std::endl;

  return 0;
}
