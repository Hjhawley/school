#include "ascii_functions.h"
#include <iostream>
#include <vector>

int main() {
  std::vector<int> picture;
  int height;
  int width;
  
  load_picture_1(picture, height, width);
  display_picture(std::cout, picture, height, width);
  
  return 0;
}
