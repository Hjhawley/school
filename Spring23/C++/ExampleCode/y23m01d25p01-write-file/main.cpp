#include <fstream>

int main() {
  std::ofstream bits("bit-patterns.txt"); // creates an output stream, associated with the file bit-patterns.txt

  int i;
  for(i = 0; i < 256; i++) {
    unsigned char byte;
    byte = (unsigned char)i;
    bits.write((char *)&byte, 1);
  }

  bits.close();
  return 0;
}
