#include <iostream>

void by_copy(int y) {
  std::cout << y << std::endl;
  std::cout << "by_copy: &y: " << &y << std::endl;
  //y = 2; // would not change x
}

void by_reference(int& y) {
  std::cout << y << std::endl;
  std::cout << "by_reference: &y: " << &y << std::endl;
  //y = 2; // would change x
}

void by_pointer(int *y) {
  std::cout << *y << std::endl;
  std::cout << "by_pointer: y: " << y << std::endl;
  std::cout << "by_pointer: &y: " << &y << std::endl;
  //*y = 2; // would change x
}

int main() {
  int x;
  x = 1;

  std::cout << "&x: " << &x << std::endl;
  by_copy(x);
  by_reference(x);
  by_pointer(&x);

  return 0;
}
