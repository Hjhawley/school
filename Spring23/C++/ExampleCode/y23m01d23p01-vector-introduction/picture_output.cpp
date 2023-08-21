#include "ascii_functions.h"

void display_picture(std::ostream& os, const std::vector<int>& picture, const int& height, const int& width) {
  int i, row, column;
  for(row = 0; row < height; row++) {
    for(column = 0; column < width; column++) {
      i = row*width  + column;
      os << (char)picture[i];
    }
    os << std::endl;
  }
}
