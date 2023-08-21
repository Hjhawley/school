#include "ascii_functions.h"

void load_picture_1(std::vector<int>& picture, int& height, int& width) {
  const std::string data = "             _.-````'-,_                 _,.,_ ,-'`           `'-.,_         /)     (\\                   '``-.    ((      ) )                      `\\    \\)    (_/                        )\\    |       /)           '    ,'    / \\   `\\    ^'            '     (    /  ))    |      _/\\ ,     /    ,,`\\   (  \"`     \\Y,   |  \\  \\  | ````| / \\_ \\           `)_/    \\  \\  )    ( >  ( >                    \\( \\(     |/   |/         mic & dwb  /_(/_(    /_(  /_(     ";
  height = 12;
  width = 38;
  int size = height*width;
  picture.resize(size);
  int i, j, row, column;
  j = 0;
  for(row = 0; row < height; row++) {
    for(column = 0; column < width; column++) {
      i = row*width + column;
      picture[i] = data[j];
      j++;
    }
  }
}
