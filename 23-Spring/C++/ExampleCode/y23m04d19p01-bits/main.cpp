#include <iostream>
#include <sstream>

int main() {
  unsigned char n = 0;
  char b1   = 1;
  char b2   = 1 << 1;
  char b4   = 1 << 2;
  char b8   = 1 << 3;
  char b16  = 1 << 4;
  char b32  = 1 << 5;
  char b64  = 1 << 6;
  char b128 = 1 << 7;
  n = b1 | b2 | b4 | b16;
  std::cout << (int)n << std::endl;

  n = b2 | b4 | b16 | b32 | b128;
  std::cout << (int)n << std::endl;

  n = b2 + b4 + b16 + b32 + b128;
  std::cout << (int)n << std::endl;

  int bign = b2 + b4 + b16 + b32 + b128;
  std::cout << bign << std::endl;

  std::cout << (int)b128 << std::endl;

  std::stringstream bitpattern;
  n = 254;
  if(n & b128) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b64) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b32) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b16) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b8) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b4) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b2) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  if(n & b1) {
    bitpattern << "1";
  } else {
    bitpattern << "0";
  }
  std::cout << bitpattern.str() << std::endl;

  {
    unsigned char a = 123;
    unsigned char b = 234;
    unsigned char c = a ^ b;
    std::cout << (int)c << std::endl;
  }

  {
    unsigned int z = 255;
    while(z > 0) {
      std::cout << (int) z << std::endl;
      z = z >> 1;
    }
  }
  

  return 0;
}
